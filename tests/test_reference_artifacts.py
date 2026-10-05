"""Reference tool requests preserve provenance and require reviewed dependencies."""

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("reference_artifacts", REPO / "scripts/reference-artifacts.py")
ART = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ART)


class ReferenceArtifactsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.episode = self.repo / "episodes/999-art-test"
        (self.episode / "plan").mkdir(parents=True)
        self.style = self.repo / "assets/styles/master.png"
        self.style.parent.mkdir(parents=True)
        Image.new("RGB", (90, 160), "gray").save(self.style)
        self.prompt = self.repo / "prompts/image/episodes/999-art-test/scene.md"
        self.prompt.parent.mkdir(parents=True)
        self.prompt.write_text("One scene, one drawn person, no panels or text.\n")
        self.state = {"stages": [{"id": k, "status": "approved"} for k in ("scenario-script", "storyboard")]}
        (self.episode / "pipeline-state.json").write_text(json.dumps(self.state))
        self.manifest = {"entries": [{"id": "scene", "prompt_repo_path": str(self.prompt.relative_to(self.repo)),
                                      "storyboard_panel_ids": ["S01"], "dependencies": []}]}
        self.manifest_path = self.episode / "plan/reference-manifest.json"
        self.manifest_path.write_text(json.dumps(self.manifest))

    def freeze(self):
        return ART.freeze(self.repo, self.episode, ["scene"], "r001", "scenes", "assets/styles/master.png")

    def test_frozen_inputs_detect_changes_and_cannot_be_replaced(self):
        request = self.freeze()
        before = request.read_bytes()
        ART.verify(self.repo, request)
        with self.assertRaises(FileExistsError):
            self.freeze()
        self.assertEqual(request.read_bytes(), before)
        self.prompt.write_text("An entirely different scene")
        with self.assertRaises(ValueError):
            ART.verify(self.repo, request)
        self.assertEqual(request.read_bytes(), before)

    def test_unreviewed_or_changed_dependency_prevents_generation_preparation(self):
        dependency = self.repo / "assets/episodes/999-art-test/references/person-r001.png"
        dependency.parent.mkdir(parents=True)
        Image.new("RGB", (90, 160), "blue").save(dependency)
        self.manifest["entries"][0]["dependencies"] = ["person"]
        person = {"id": "person", "selected_path": str(dependency.relative_to(self.repo)),
                  "sha256": hashlib.sha256(dependency.read_bytes()).hexdigest(), "review_status": "needs_review"}
        self.manifest["entries"].append(person)
        self.manifest_path.write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):
            self.freeze()
        person.update(review_status="approved", review_decision={"reviewer": "fixture", "notes": "Fixture review"})
        self.manifest_path.write_text(json.dumps(self.manifest))
        request = self.freeze()
        Image.new("RGB", (90, 160), "red").save(dependency)
        with self.assertRaises(ValueError):
            ART.verify(self.repo, request)

    def test_ingest_preserves_candidate_bytes_without_selecting_or_approving(self):
        request = self.freeze()
        source = self.repo / "generated.png"
        Image.new("RGB", (90, 160), "green").save(source)
        original = source.read_bytes()
        manifest_before = self.manifest_path.read_bytes()
        image, record = ART.ingest(self.repo, self.episode, request, "scene", source)
        self.assertEqual(image.read_bytes(), original)
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(self.manifest_path.read_bytes(), manifest_before)
        self.assertEqual(json.loads(record.read_text())["review_status"], "needs_review")
        with self.assertRaises(FileExistsError):
            ART.ingest(self.repo, self.episode, request, "scene", source)
        self.assertEqual(image.read_bytes(), original)

    def test_excess_image_inputs_fail_before_request_or_tool_call(self):
        self.manifest["entries"][0]["content_images"] = [
            {"path": "assets/styles/master.png", "role": f"content {i}"} for i in range(5)
        ]
        self.manifest_path.write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(ValueError, "at most five"):
            self.freeze()
        self.assertFalse((self.episode / "plan/references/scenes-requests-r001.json").exists())


if __name__ == "__main__":
    unittest.main()
