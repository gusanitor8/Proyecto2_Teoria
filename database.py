from neo4j import GraphDatabase
from Variable import Symbol
from typing import Set

URI = "bolt://localhost:7687"  # Replace with your Neo4j database URI
USERNAME = "neo4j"  # Replace with your Neo4j username
PASSWORD = "12345678"  # Replace with your Neo4j password


class Database:
    def __init__(self, uri=URI, username=USERNAME, password=PASSWORD):
        self._driver = GraphDatabase.driver(uri, auth=(username, password))

    def __open_session(self):
        return self._driver.session()

    @staticmethod
    def __close_session(session):
        session.close()

    def instanciate_nodes(self, symbols: Set[Symbol]):
        """
        Se crean todos los nodos en la base de datos y posteriormente se crea una relacion entre los que tienen
        reglas unitarias

        :param symbols: un conjunto de simbolos
        :return:
        """
        session = self.__open_session()

        try:
            self.__create_nodes(symbols, session)
            self.__create_relation(symbols, session)
        finally:
            self.__close_session(session)

    def __create_nodes(self, symbols: Set[Symbol], session):
        """
        Se crean los nodos en la base de datos

        :param symbols: conjunto de simbolos
        :param session: sesion de la base de datos
        :return: None
        """

        def create_node(tx, node_id, node_symbol):
            create_node_query = """
            CREATE (n:Symbol {id: $node_id, symbol: $node_symbol})
            """
            result = tx.run(create_node_query, node_id=node_id, node_symbol=node_symbol)
            return result

        for symbol in symbols:
            created_node = session.write_transaction(create_node, symbol.id, symbol.symbol)

    def __create_relation(self, symbols : Set[Symbol], session):
        """
        Se crean las relaciones entre los nodos de la base de datos

        :param symbols: conjunto de simbolos
        :param session: sesion de la base de datos
        :return:
        """
        def create_relation(tx, node_id1, node_symbol1, node_id2, node_symbol2):
            relation_query = """
            MATCH (a:Symbol {symbol: $node_symbol1})
            MATCH (b:Symbol {symbol: $node_symbol2})
            CREATE (a)-[r:PRODUCES]->(b)
            RETURN a,b
            """

            result = tx.run(relation_query, node_id1=node_id1, node_symbol1=node_symbol1, node_id2=node_id2,
                            node_symbol2=node_symbol2)
            return result

        for symbol in symbols:
            for production in symbol.get_unit_productions():
                created_relation = session.write_transaction(create_relation,
                                                             symbol.id, symbol.symbol,
                                                             production[0].id, production[0].symbol)

    def get_reachable_nodes(self, symbol: Symbol):
        """
        Dado un solo simbolo, nos devuelve los nodos alcanzables a traves de reglas unitarias en uno o mas pasos

        :param symbol: Symbol
        :return: conjunto de los ids de los nodos alcanzables a traves de reglas unitarias
        """
        def get_reachable_nodes(tx, symbol1):
            query = """
            MATCH (n:Symbol{symbol:$symbol1})
            WITH n AS startNode
            MATCH (startNode)-[*1..]->(reachableNode)
            RETURN COLLECT(DISTINCT reachableNode) AS allReachableNodes
            """
            return tx.run(query, symbol1=symbol1)

        reachable_nodes_id = set()
        session = self.__open_session()
        try:
            with session.begin_transaction() as tx:
                result = get_reachable_nodes(tx, symbol.get_symbol())

                # Process the result within the transaction context
                for record in result:
                    all_reachable_nodes = record["allReachableNodes"]

                    # Now you can work with the list of reachable nodes
                    for node in all_reachable_nodes:
                        # TODO quitar el print
                        print(node_id := node.get("id"))
                        reachable_nodes_id.add(node_id)

                return reachable_nodes_id
        finally:
            self.__close_session(session)

    def clear_database(self):
        """
        Borra todos los nodos y relaciones de la base de datos para poder volver a instanciarlos
        en la siguiente ejecucion del programa

        :return: None
        """

        def clear_database(tx):
            query = """
            MATCH (n)
            DETACH DELETE n
            """
            return tx.run(query)

        session = self.__open_session()

        try:
            session.write_transaction(clear_database)
        finally:
            self.__close_session(session)
