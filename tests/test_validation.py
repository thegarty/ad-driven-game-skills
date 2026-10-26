import importlib.util
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location("validator", Path(__file__).resolve().parents[1] / "scripts/validate_library.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.skill = Path(self.tmp.name) / "demo"
        self.skill.mkdir()
        (self.skill / "LICENSE").write_text("MIT")
        self.prefix = '---\nname: demo\ndescription: "Make a useful artifact."\nlicense: MIT\n---\n'
        self.write("# Demo\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text):
        (self.skill / "SKILL.md").write_text(self.prefix + text)

    def test_standalone_skill(self):
        (self.skill / "guide.md").write_text("Useful content")
        self.write("[Guide](guide.md) and [Official docs](https://example.org/reference).")
        self.assertEqual(validator.validate_skill(self.skill), [])

    def test_missing_reference(self):
        self.write("[Guide](references/missing.md)")
        self.assertTrue(any("missing linked" in e for e in validator.validate_skill(self.skill)))

    def test_sibling_dependency_rejected(self):
        self.write("[Sibling](../other/SKILL.md)")
        self.assertTrue(any("escapes" in e for e in validator.validate_skill(self.skill)))

    def test_directory_name_must_match(self):
        self.prefix = self.prefix.replace("name: demo", "name: different")
        self.write("Body")
        self.assertTrue(any("match" in e for e in validator.validate_skill(self.skill)))

    def test_empty_description(self):
        self.prefix = self.prefix.replace('"Make a useful artifact."', '""')
        self.write("Body")
        self.assertTrue(any("description" in e for e in validator.validate_skill(self.skill)))

    def test_duplicate_frontmatter_key(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validator.frontmatter("---\nname: a\nname: b\n---\n")

    def test_template_with_spaces_in_path(self):
        (self.skill / "my template.md").write_text("Template")
        self.write("[Template](<my template.md>)")
        self.assertEqual(validator.validate_skill(self.skill), [])


if __name__ == "__main__":
    unittest.main()
