def insert_nodes(database, nodes):

    def txn(tx):

        for node in nodes:

            #table = node.pop("table")
            table = node["table"]
            data = {k: v for k, v in node.items() if k != "table"}

            tx.insert_or_update(
                table,
                columns=list(data.keys()),
                values=[tuple(data.values())]
            )

    database.run_in_transaction(txn)


def insert_edges(database, edges):

    def txn(tx):

        for edge in edges:

            #table = edge.pop("table")
            table = edge["table"]
            data = {k: v for k, v in edge.items() if k != "table"}

            tx.insert_or_update(
                table,
                columns=list(data.keys()),
                values=[tuple(data.values())]
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