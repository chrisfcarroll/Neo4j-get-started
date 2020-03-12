from neo4j import GraphDatabase

# See https://neo4j.com/developer/python
class Neo(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
    def close(self):
        self._driver.close()
    def run(self,command):
        with self._driver.session() as session:
            result = session.write_transaction(lambda tx: tx.run(command))
            return result
    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)
    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]
    @staticmethod
    def _run(tx, command):
        result=tx.run(command)
        return result
