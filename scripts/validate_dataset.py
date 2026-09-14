"""Validate the record structure; does not assess clinical quality or call models."""
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path


def validate_questions(path):
    errors, ids = [], set()
    required = {'question_id', 'topic', 'question', 'risk_level', 'origin', 'review_status'}
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not required.issubset(set(reader.fieldnames or [])):
            return ids, ['questions: missing required CSV columns']
        count = 0
        for row_number, row in enumerate(reader, 2):
            count += 1
            prefix = f'questions:{row_number}'
            for key in required:
                if not isinstance(row.get(key), str) or not row[key].strip():
                    errors.append(f'{prefix}: empty {key}')
            qid = (row.get('question_id') or '').strip()
            if qid in ids:
                errors.append(f'{prefix}: duplicate question_id')
            if qid:
                ids.add(qid)
            if row.get('risk_level') not in {'low', 'medium', 'high'}:
                errors.append(f'{prefix}: invalid risk_level')
        if count == 0:
            errors.append('questions: no records')
    return ids, errors


def validate_answers(path, question_ids):
    errors, seen = [], set()
    required = {'run_id', 'question_id', 'batch_id', 'repeat_index', 'platform',
                'model', 'model_version', 'entry_type', 'network_enabled',
                'run_at', 'status', 'answer_text', 'error', 'citations',
                'synthetic', 'scoring_status'}
    text_fields = {'run_id', 'question_id', 'batch_id', 'platform', 'model',
                   'model_version', 'entry_type', 'run_at'}
    count = 0
    with Path(path).open(encoding='utf-8') as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            count += 1
            prefix = f'answers:{line_number}'
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                errors.append(f'{prefix}: invalid JSON')
                continue
            if not isinstance(row, dict):
                errors.append(f'{prefix}: expected object')
                continue
            missing = required - row.keys()
            if missing:
                errors.append(f'{prefix}: missing {", ".join(sorted(missing))}')
            for key in text_fields:
                if not isinstance(row.get(key), str) or not row[key].strip():
                    errors.append(f'{prefix}: invalid {key}')
            rid = row.get('run_id')
            if isinstance(rid, str):
                if rid in seen:
                    errors.append(f'{prefix}: duplicate run_id')
                seen.add(rid)
            qid = row.get('question_id')
            if not isinstance(qid, str) or qid not in question_ids:
                errors.append(f'{prefix}: unknown question_id')
            repeat = row.get('repeat_index')
            if type(repeat) is not int or repeat < 1:
                errors.append(f'{prefix}: repeat_index must be a positive integer')
            for key in ('network_enabled', 'synthetic'):
                if type(row.get(key)) is not bool:
                    errors.append(f'{prefix}: {key} must be boolean')
            if not isinstance(row.get('citations'), list):
                errors.append(f'{prefix}: citations must be an array')
            try:
                stamp = datetime.fromisoformat(str(row.get('run_at', '')).replace('Z', '+00:00'))
                if stamp.tzinfo is None or stamp.utcoffset() is None:
                    raise ValueError('missing timezone')
            except ValueError:
                errors.append(f'{prefix}: run_at must include a valid time and timezone')
            status = row.get('status')
            if status not in {'success', 'failed'}:
                errors.append(f'{prefix}: invalid status')
            if status == 'success' and (not isinstance(row.get('answer_text'), str) or not row['answer_text'].strip()):
                errors.append(f'{prefix}: successful run needs answer_text')
            if status == 'failed' and (not isinstance(row.get('error'), str) or not row['error'].strip()):
                errors.append(f'{prefix}: failed run needs error')
            if row.get('scoring_status') not in {'not_scored', 'scored'}:
                errors.append(f'{prefix}: invalid scoring_status')
    if count == 0:
        errors.append('answers: no records')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('questions', type=Path)
    parser.add_argument('answers', type=Path)
    args = parser.parse_args()
    try:
        ids, errors = validate_questions(args.questions)
        errors.extend(validate_answers(args.answers, ids))
    except (OSError, UnicodeError, csv.Error) as error:
        print(f'Unable to read dataset: {error}')
        return 2
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'PASS: {len(ids)} questions; answer record structure valid. Clinical quality was not assessed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
