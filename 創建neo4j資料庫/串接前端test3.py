from neo4j import GraphDatabase

def search_nodes_related_to_card(tx, input_string):
    query = (
        "MATCH (n:Categorical)-[:RELATED_TO]->(b) "
        "WHERE n.name CONTAINS $input_string "
        "WITH n, b, CASE WHEN b:Categorical THEN 'categorical' ELSE 'other' END as nodeType "
        "OPTIONAL MATCH (b)-[:reward]->(reward_card:card) "
        "WITH n, b, nodeType, reward_card "
        "RETURN n, b, nodeType, reward_card"
    )

    result = tx.run(query, input_string=input_string)
    return result.data()

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "Test1022"))

input_string = "蝦皮"
with driver.session() as session:
    result_data = session.read_transaction(search_nodes_related_to_card, input_string)

# 處理查詢結果
for record in result_data:
    print(record)

# 關閉 Neo4j 連線
driver.close()
