import json
import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import db
from models.account import Account

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    from models import app, db
    
    with app.app_context():
        db.create_all()
        yield
        db.session.close()

class TestAccountModel:
    """Modelo de pruebas de cuenta"""

    @classmethod
    def setup_class(cls):
        """Conectar y cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        import os
        current_dir = os.path.dirname(__file__)
        fixture_path = os.path.join(current_dir, 'fixtures', 'account_data.json')
        with open(fixture_path) as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos"""
        pass  # Agrega cualquier acción de limpieza si es necesario

    def setup_method(self):
        """Truncar las tablas antes de cada prueba"""
        db.session.query(Account).delete()
        db.session.commit()

    def teardown_method(self):
        """Eliminar la sesión después de cada prueba"""
        db.session.remove()

    #  Casos de prueba
    def test_create_an_account(self):
        """Probar la creación de una sola cuenta"""
        data = ACCOUNT_DATA[0]  # obtener la primera cuenta
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1

    def test_create_all_accounts(self):
        """Probar la creación de múltiples cuentas"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        assert len(Account.all()) == len(ACCOUNT_DATA)
