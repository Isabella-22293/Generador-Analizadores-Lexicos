import os

class Visualizer:
    def graph_afd(self, afd_converter, output_path):
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("AFD Graph Placeholder\n")
            f.write("AFN List:\n")
            for token, afn in afd_converter.afn_list.items():
                f.write(f"{token}: {afn}\n")
        print(f"Gráfico del AFD guardado en {output_path}")
