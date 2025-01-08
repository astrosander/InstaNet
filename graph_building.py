import os
import pickle  # <-- Use Pickle for saving
import json
import networkx as nx
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from fa2 import ForceAtlas2

# Path to the folder containing JSON files
data_folder = "selective"

we_accept = ['15625857219.json', '65790280522.json', '8257259395.json', '44106592788.json', '62219323705.json', '51127265402.json', '13007508362.json', '7559527896.json', '60363993714.json', '3304581194.json', '50763355894.json', '3444535015.json', '60045503574.json', '1431456321.json', '58028828892.json', '14341459266.json', '26489379880.json', '3452354466.json', '60046618452.json', '12345772435.json', '46291109738.json', '47539118096.json', '57634412315.json', '12252150141.json', '59616444701.json', '58526278666.json', '21908584046.json', '2025109518.json', '6426461640.json', '8318971688.json', '8644202180.json', '4381575285.json', '742177410.json', '8489857177.json', '36565404192.json', '12395837239.json', '52934754237.json', '44949452857.json', '7244805283.json', '14328531437.json', '44663751199.json', '59696291718.json', '70354757842.json', '12663996904.json', '55546222047.json', '59685289457.json', '21887504461.json', '44841794558.json', '6018373947.json', '18342816684.json', '3950109868.json', '7170321740.json', '25516833418.json', '8239100611.json', '8548794015.json', '52135115488.json', '203827442.json', '8577316008.json', '1589452400.json', '3406489092.json', '46598625471.json', '9150696176.json', '54527659870.json', '6795842361.json', '26044102730.json', '8285480615.json', '13368024716.json', '48609606327.json', '10228806343.json', '6704172084.json', '25036582558.json', '56005565188.json', '6426007242.json', '7726276852.json', '1127216523.json', '2004204354.json', '31921806750.json', '44982232660.json', '1356931231.json', '7523918828.json', '22363279600.json', '32780617730.json', '32193551227.json', '6752067103.json', '28367612395.json', '13037920531.json', '13392538099.json', '25134173744.json', '58769030058.json', '16514304079.json', '4363682780.json', '7374026143.json', '2587102090.json', '11797297112.json', '5623014821.json', '35193420933.json', '64687201434.json', '342069970.json', '8132328158.json', '4365205299.json', '49740327659.json', '38457167948.json', '48856022677.json', '55693617037.json', '54434223243.json', '6842814301.json', '9843915671.json', '10160094222.json', '3006345097.json', '39917423720.json', '44288486979.json', '45132628095.json', '13328150432.json', '13035512719.json', '1934654486.json', '40252926802.json', '5688344379.json', '60807330947.json', '2143706220.json', '3511646437.json', '5348325703.json', '3579284776.json', '66392972313.json', '18043982059.json', '312068892.json', '54696518383.json', '21241788494.json', '6160643484.json', '3033360627.json', '57095227530.json', '61125818098.json', '18026333157.json', '3578543670.json', '65216006940.json', '6679878120.json', '31542142110.json', '45026581654.json', '61318431167.json', '3772158384.json', '455706821.json', '9645984578.json', '19795552590.json', '15049805116.json', '2044077761.json', '3708311533.json', '58493046832.json', '9767444753.json', '2560693901.json', '14430423721.json', '3237268994.json', '8212364304.json', '19945195411.json', '25337303738.json', '3784783579.json', '55873818427.json', '1188220357.json', '2206621638.json', '27167085367.json', '46447809863.json', '4784070081.json', '8250563666.json', '8976309310.json', '41551361893.json', '4184967574.json', '44550299489.json', '6161412822.json', '8031220658.json', '45997617983.json', '7814217461.json', '11824117626.json', '52522142700.json', '54602315643.json', '31467813473.json', '49249081981.json', '6876795545.json', '7557084159.json', '1745669945.json', '21479090103.json', '456397329.json', '3430595982.json', '64061188448.json', '13356960821.json', '15701270411.json', '25450745569.json', '4181150619.json', '42758579279.json', '466625675.json', '54488309072.json', '8968406889.json', '13788660269.json', '44446047477.json', '49232204787.json', '5844485247.json', '6275795571.json', '8517699843.json', '13839262659.json', '1804308241.json', '24000580644.json', '44425586111.json', '3429289166.json', '50239185614.json', '52409121958.json', '6917226104.json', '7734292940.json', '1459563706.json', '2022901196.json', '54352819360.json', '8918038961.json', '10982693742.json', '2374911101.json', '8594898462.json', '10616580373.json', '40531473486.json', '7377102268.json', '16701030715.json', '63850070590.json', '17415939917.json', '45375696821.json', '48202205172.json', '5727013619.json', '19219511067.json', '263517312.json', '3481399275.json', '35212440524.json', '61339392815.json', '7190752611.json', '57124208904.json', '58080180942.json', '59141868120.json', '13237337155.json', '49038571520.json', '49275947930.json', '35688950188.json', '41324739822.json', '4581054990.json', '9248454286.json', '1617110104.json', '56341359676.json', '59481841863.json', '1972883224.json', '39635616050.json', '54611853639.json', '5932275319.json', '6804393539.json', '8673719691.json', '26046884545.json', '28925698614.json', '38702876687.json', '5645508021.json', '6260714933.json', '59077313838.json', '59139266175.json', '65095429819.json', '7709925597.json', '246605512.json', '6665993849.json', '6936357876.json', '7766933108.json', '8195424216.json', '313816756.json', '3411389275.json', '36356033814.json', '54510394269.json', '59867044450.json', '9227897576.json', '19798953014.json', '32913265089.json', '53042194174.json', '54097540231.json', '573498801.json', '6048469400.json', '41429726231.json', '4579874871.json', '50290978936.json', '54517695777.json', '6817173579.json', '6876219188.json', '24637634270.json', '5237223420.json', '59932659994.json', '24567137564.json', '47304177945.json', '50196183781.json', '17855591407.json', '27492507134.json', '3426578033.json', '53309629237.json', '57869232044.json', '11297740492.json', '475533863.json', '52582081565.json', '6788707125.json', '53701716118.json', '6194741334.json', '12609170917.json', '21621235277.json', '2288095458.json', '4478365359.json', '45245668850.json', '7792135363.json']


# Function to process a single file and return edges
def process_file(file_path):
    edges = []
    user_id = os.path.basename(file_path).split(".")[0]
    with open(file_path, 'r', encoding='utf-8') as f:
        follow_data = json.load(f)
        for entry in follow_data:
            followed_id = entry["id"]
            edges.append((user_id, followed_id))
    return edges

# Main function to handle parallel processing and graph building
def main():
    G = nx.Graph()

    # Use all available CPU cores
    max_workers = cpu_count()

    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        json_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".json") and f in we_accept]
        
        results = executor.map(process_file, json_files)

    # Add edges to the graph in batches
    for edges in results:
        G.add_edges_from(edges)


    # Compute node degrees
    degrees = dict(G.degree())
    max_degree = max(degrees.values()) if degrees else 0.1



    # Use a layout suitable for large graphs

    # pos = nx.kamada_kawai_layout(G, weight=None) #106.2s

    # pos = nx.spring_layout(G, seed=42) #18 second
    
    print('lol')
    from fa2 import ForceAtlas2
    
    forceatlas2 = ForceAtlas2(
        outboundAttractionDistribution=True,
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        scalingRatio=2.0,
        gravity=1.0,
        verbose=True
    )

    pos = forceatlas2.forceatlas2_networkx_layout(G, iterations=2000)


    # pos = nx.spring_layout(G, seed=42)#27.8s

    print('lol')

    # Define the node size based on degree (scaled)
    node_sizes = [degrees[node] * 0.1 for node in G.nodes()]


    with open("trained_pickle\\pos.pkl", "wb") as f:
        pickle.dump(pos, f)

    with open("trained_pickle\\G.pkl", "wb") as f:
        pickle.dump(G, f)

    with open("trained_pickle\\node_sizes.pkl", "wb") as f:
        pickle.dump(node_sizes, f)


    # Plot the graph in chunks to reduce memory usage
    plt.figure(figsize=(200, 15))
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=node_sizes,
        cmap=plt.cm.plasma, 
        alpha=0.4
    )
    nx.draw_networkx_edges(G, pos, alpha=0.001)

    plt.title("Follower Graph Heatmap")
    plt.axis("off")
    plt.show()


    print("Layout saved to forceatlas2_layout.pkl")

if __name__ == '__main__':
    main()
