from ..utils import hash, verify_credentials

def test_hash_funct():
    test_password = 'password'
    hashed_password = hash(test_password)
    
    assert hashed_password != test_password
    assert isinstance(hashed_password, str)
    assert hashed_password is not None
    assert len(hashed_password) > 0

    
def test_verify_credentials_funct():
    test_password = 'password'
    hashed_password = hash(test_password)

    assert verify_credentials(test_password, hashed_password) is True
    assert verify_credentials("wrongpassword", hashed_password) is False
