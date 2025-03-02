import hashlib

def hash_string(input_string):
    """
    Calcule le hash SHA-256 de la chaîne d'entrée.
    On encode la chaîne en UTF-8 puis on retourne la valeur hexadécimale.
    """
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

def sign_hash(privateKey, hash_value):
    """
    Simule une signature en concaténant la clé privée et le hash,
    puis en calculant le hash de la chaîne obtenue.
    (Cette méthode est uniquement illustrative et non sécurisée.)
    """
    return hash_string(privateKey + hash_value)

def has_public_key_signed_this_hash(publicKey, signature, hash_value):
    """
    Vérifie que la signature correspond bien au hash fourni.
    Pour la simulation, nous considérons que la signature doit être égale
    au hash de la concaténation de la clé publique et du hash.
    
    Si la signature est vide, la vérification échoue.
    """
    if signature == '':
        return False
    expected_signature = hash_string(publicKey + hash_value)
    return signature == expected_signature

def get_black_hole_public_key():
    """
    Retourne une clé publique spéciale servant à créer le bloc genesis.
    """
    return "BLACK_HOLE_PUBLIC_KEY"

def get_default_hash():
    """
    Retourne un hash par défaut (ici 64 zéros) utilisé pour le bloc genesis
    qui n'a pas de bloc parent.
    """
    return "0" * 64
