from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *
from pymongo import *
import unittest
from model import Patient


class TestStringMethods(unittest.TestCase):

  def test_upper(self):

      # This connections to the DB and starts the session
      session = Session.connect('easyris')
      session.clear_collection(Patient) # clear previous runs of this code!
      # Insert on a session will infer the correct collection and push the object
      # into the database


      me = Patient(first_name='Piero', last_name='Chiacchiaretta',
      birthdate=datetime(year=1979, day=27, month=9), birthplace='AGRIGENTO', cf_code='CHCPRI79P27G482U',
      gender="M", address='Via Aldo Moro, 114', city='San Giovanni Teatino', province='Chieti',
      CAP=66020, phone_number='3294946261', email='piero.chiacchiaretta@gmail.com', nationality='italiana')

      me = Patient(id_patient=me.id_calc,first_name='Piero', last_name='Chiacchiaretta',
      birthdate=datetime(year=1979, day=27, month=9), birthplace='AGRIGENTO', cf_code='CHCPRI79P27G482U',
      gender="M", address='Via Aldo Moro, 114', city='San Giovanni Teatino', province='Chieti',
      CAP=66020, phone_number='3294946261', email='piero.chiacchiaretta@gmail.com', nationality='italiana',
      age= me.age_calc, cf_calc=me.cf_code_calc)

      session.save(me)

      you = Patient(first_name='Riccardo', last_name='Navarra',
      birthdate=datetime(year=1972, day=10, month=9), birthplace='L\'AQUILA', cf_code='NVRRCR7210345G',
      gender="M", address='Via G. Carducci, 25', city='L\'Aquila', province='L\'Aquila',
      CAP=66020, phone_number='3294946261', email='riccardo.navarra@gmail.com', nationality='italiana')

      you = Patient(id_patient=you.id_calc,first_name='Riccardo', last_name='Navarra',
      birthdate=datetime(year=1972, day=10, month=9), birthplace='L\'AQUILA', cf_code='NVRRCR7210345G',
      gender="M", address='Via G. Carducci, 25', city='L\'Aquila', province='L\'Aquila',
      CAP=66020, phone_number='3294946261', email='riccardo.navarra@gmail.com', nationality='italiana',
      age= you.age_calc, cf_calc=you.cf_code_calc)

      session.save(you)

      client = MongoClient()
      db = client.easyris
      result=db.get_collection('patients').find({'first_name' :me.first_name})
      result2=result.next()
      test=result2['first_name']
      self.assertEqual(me.first_name, str(test))
      test=result2['id_patient']
      self.assertEqual(me.id_patient, str(test))
      test=result2['cf_calc']
      self.assertEqual(me.cf_calc, str(test))



  # def test_isupper(self):
  #     self.assertTrue('FOO'.isupper())
  #     self.assertFalse('Foo'.isupper())
  #
  # def test_split(self):
  #     s = 'hello world'
  #     self.assertEqual(s.split(), ['hello', 'world'])
  #     # check that s.split fails when the separator is not a string
  #     with self.assertRaises(TypeError):
  #         s.split(2)

if __name__ == '__main__':
    unittest.main()
