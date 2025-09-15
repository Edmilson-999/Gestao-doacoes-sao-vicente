import pytest
from src.models import Beneficiario  # Note o import relativo

def test_beneficiario_creation():
    benef = Beneficiario(nif='test', nome='Test Name')
    assert benef.nif == 'test'
    assert benef.nome == 'Test Name'