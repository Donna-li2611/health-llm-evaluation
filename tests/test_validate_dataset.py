import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate_dataset.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class DatasetValidationTests(unittest.TestCase):
    def setUp(self):
        self.sample = json.loads((ROOT / 'examples/answers.synthetic.jsonl').read_text(encoding='utf-8'))

    def check_rows(self, rows):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'answers.jsonl'
            target.write_text('\n'.join(json.dumps(row) for row in rows), encoding='utf-8')
            return validator.validate_answers(target, {'Q001'})

    def test_public_demo_is_structurally_valid(self):
        ids, errors = validator.validate_questions(ROOT / 'data/questions.csv')
        self.assertEqual(20, len(ids))
        self.assertEqual([], errors)
        self.assertEqual([], validator.validate_answers(ROOT / 'examples/answers.synthetic.jsonl', ids))

    def test_duplicate_runs_cannot_silently_inflate_sample(self):
        self.assertTrue(any('duplicate run_id' in e for e in self.check_rows([self.sample, self.sample])))

    def test_unknown_question_is_rejected(self):
        self.sample['question_id'] = 'MISSING'
        self.assertTrue(any('unknown question_id' in e for e in self.check_rows([self.sample])))

    def test_failed_run_preserves_error(self):
        self.sample.update(status='failed', answer_text='', error='timeout')
        self.assertEqual([], self.check_rows([self.sample]))
        self.sample['error'] = ''
        self.assertTrue(any('failed run needs error' in e for e in self.check_rows([self.sample])))

    def test_timestamp_requires_timezone(self):
        self.sample['run_at'] = '2026-09-14T12:00:00'
        self.assertTrue(any('timezone' in e for e in self.check_rows([self.sample])))

    def test_empty_success_and_boolean_repeat_are_rejected(self):
        self.sample.update(answer_text='', repeat_index=True)
        errors = self.check_rows([self.sample])
        self.assertTrue(any('needs answer_text' in e for e in errors))
        self.assertTrue(any('positive integer' in e for e in errors))

    def test_unhashable_ids_report_errors_instead_of_crashing(self):
        self.sample.update(run_id=[], question_id={})
        errors = self.check_rows([self.sample])
        self.assertTrue(any('invalid run_id' in e for e in errors))
        self.assertTrue(any('unknown question_id' in e for e in errors))

    def test_empty_questions_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'questions.csv'
            target.write_text('question_id,topic,question,risk_level,origin,review_status\n', encoding='utf-8')
            _, errors = validator.validate_questions(target)
            self.assertIn('questions: no records', errors)


if __name__ == '__main__':
    unittest.main()
