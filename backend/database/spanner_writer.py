def insert_nodes(database, nodes):

    def txn(tx):

        for node in nodes:

            table = node.pop("table")

            tx.insert_or_update(
                table,
                columns=list(node.keys()),
                values=[tuple(node.values())]
            )

    database.run_in_transaction(txn)


def insert_edges(database, edges):

    def txn(tx):

        for edge in edges:

            table = edge.pop("table")

            tx.insert_or_update(
                table,
                columns=list(edge.keys()),
                values=[tuple(edge.values())]
            )

    database.run_in_transaction(txn)


# def insert_nodes(database, nodes):

#     with database.batch() as batch:

#         for node in nodes:
#             table = node["table"]
#             data = node["data"]

#             batch.insert_or_update(
#                 table=table,
#                 columns=list(data.keys()),
#                 values=[tuple(data.values())],
#             )


# def insert_edges(database, edges):

#     with database.batch() as batch:

#         for edge in edges:
#             table = edge["table"]
#             data = edge["data"]

#             batch.insert_or_update(
#                 table=table,
#                 columns=list(data.keys()),
#                 values=[tuple(data.values())],
#             )