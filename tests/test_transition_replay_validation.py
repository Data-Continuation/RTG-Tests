#!/usr/bin/env python3
"""Provisional RTG transition-replay validation tests."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
FIXTURE_PATH=ROOT/'fixtures'/'transition-replay-validation.valid.json'
VALID_REPLAY_STATES={'valid_replay','receipt_consistent','replay_required','receipt_conflict','invalid_replay','unreplayable_provisional'}
NUMERIC_FIELDS={'receipt_consistency','replay_consistency','model_visibility'}
BOOLEAN_FIELDS={'transition_claim_present','replay_attempted','replay_success','source_hash_match','target_hash_match','known_invalid_signal'}
REQUIRED_CASE_FIELDS={'case_id','expected_replay_state',*NUMERIC_FIELDS,*BOOLEAN_FIELDS}
REQUIRED_THRESHOLDS={'hash_match_required','receipt_consistency_min','replay_consistency_min','provisional_visibility_max'}
def load_fixture()->dict[str,Any]:
    with FIXTURE_PATH.open('r',encoding='utf-8') as h: payload=json.load(h)
    if not isinstance(payload,dict): raise AssertionError('Transition-replay fixture must be a JSON object.')
    return payload
def assert_unit_interval(name:str,value:Any)->None:
    if not isinstance(value,(int,float)): raise AssertionError(f'{name} must be numeric.')
    if not 0 <= float(value) <= 1: raise AssertionError(f'{name} must be between 0 and 1.')
def validate_thresholds(thresholds:dict[str,Any])->None:
    missing=sorted(REQUIRED_THRESHOLDS-set(thresholds))
    if missing: raise AssertionError(f'Missing thresholds: {missing}')
    if not isinstance(thresholds['hash_match_required'],bool): raise AssertionError('thresholds.hash_match_required must be boolean.')
    for field in REQUIRED_THRESHOLDS-{'hash_match_required'}: assert_unit_interval(f'thresholds.{field}',thresholds[field])
def validate_fixture(payload:dict[str,Any])->None:
    if set(payload.get('valid_replay_states',[])) != VALID_REPLAY_STATES: raise AssertionError('valid_replay_states must exactly match expected replay states.')
    outputs=payload.get('governance_outputs')
    if not isinstance(outputs,dict) or set(outputs)!=VALID_REPLAY_STATES: raise AssertionError('governance_outputs must define every replay state.')
    if not isinstance(payload.get('cases'),list) or not payload['cases']: raise AssertionError('cases must be a non-empty list.')
def validate_cases(payload:dict[str,Any])->None:
    seen=set()
    for index,case in enumerate(payload['cases']):
        missing=sorted(REQUIRED_CASE_FIELDS-set(case))
        if missing: raise AssertionError(f'case at index {index} missing fields: {missing}')
        case_id=case['case_id']
        if not isinstance(case_id,str) or not case_id: raise AssertionError(f'case at index {index} has invalid case_id.')
        if case_id in seen: raise AssertionError(f'duplicate case_id: {case_id}')
        seen.add(case_id)
        for field in BOOLEAN_FIELDS:
            if not isinstance(case[field],bool): raise AssertionError(f'{case_id}.{field} must be boolean.')
        for field in NUMERIC_FIELDS: assert_unit_interval(f'{case_id}.{field}',case[field])
        if case['expected_replay_state'] not in VALID_REPLAY_STATES: raise AssertionError(f'{case_id} has invalid expected_replay_state.')
        if case['replay_success'] and not case['replay_attempted']: raise AssertionError(f'{case_id} cannot have replay_success without replay_attempted.')
def classify_replay(case:dict[str,Any], thresholds:dict[str,Any])->str:
    receipt_min=float(thresholds['receipt_consistency_min']); replay_min=float(thresholds['replay_consistency_min']); provisional_max=float(thresholds['provisional_visibility_max'])
    if case['known_invalid_signal'] and float(case['receipt_consistency']) < receipt_min and not case['target_hash_match']: return 'receipt_conflict'
    if case['replay_attempted'] and not case['replay_success'] and case['known_invalid_signal']: return 'invalid_replay'
    if case['replay_attempted'] and case['replay_success'] and case['source_hash_match'] and case['target_hash_match'] and float(case['replay_consistency']) >= replay_min and float(case['receipt_consistency']) >= receipt_min: return 'valid_replay'
    if (not case['replay_attempted']) and case['source_hash_match'] and case['target_hash_match'] and float(case['receipt_consistency']) >= receipt_min: return 'receipt_consistent'
    if (not case['replay_attempted']) and float(case['model_visibility']) <= provisional_max and not case['known_invalid_signal']: return 'unreplayable_provisional'
    return 'replay_required'
def test_replay_classification(payload:dict[str,Any])->None:
    for case in payload['cases']:
        actual=classify_replay(case,payload['thresholds']); expected=case['expected_replay_state']
        if actual != expected: raise AssertionError(f"{case['case_id']} expected {expected}, got {actual}.")
def test_fixture_covers_all_replay_states(payload:dict[str,Any])->None:
    seen={case['expected_replay_state'] for case in payload['cases']}; missing=sorted(VALID_REPLAY_STATES-seen)
    if missing: raise AssertionError(f'Fixture missing replay states: {missing}')
def test_valid_replay_requires_hash_and_consistency(payload:dict[str,Any])->None:
    thresholds=payload['thresholds']
    for case in payload['cases']:
        if case['expected_replay_state']=='valid_replay':
            if not case['source_hash_match'] or not case['target_hash_match']: raise AssertionError(f"{case['case_id']} valid replay requires matching hashes.")
            if float(case['receipt_consistency']) < float(thresholds['receipt_consistency_min']): raise AssertionError(f"{case['case_id']} valid replay requires receipt consistency.")
            if float(case['replay_consistency']) < float(thresholds['replay_consistency_min']): raise AssertionError(f"{case['case_id']} valid replay requires replay consistency.")
def test_invalid_replay_and_conflict_do_not_accept_evidence(payload:dict[str,Any])->None:
    outputs=payload['governance_outputs']; accepting={'accept_state_evidence','accept_with_receipt_basis'}
    for state in ['receipt_conflict','invalid_replay']:
        if outputs[state] in accepting: raise AssertionError(f'{state} must not accept state evidence.')
def main()->None:
    payload=load_fixture()
    if not isinstance(payload.get('thresholds'),dict): raise AssertionError('Fixture must contain thresholds object.')
    validate_thresholds(payload['thresholds']); validate_fixture(payload); validate_cases(payload)
    test_fixture_covers_all_replay_states(payload); test_replay_classification(payload); test_valid_replay_requires_hash_and_consistency(payload); test_invalid_replay_and_conflict_do_not_accept_evidence(payload)
    print('RTG transition-replay validation tests passed.')
if __name__=='__main__': main()
