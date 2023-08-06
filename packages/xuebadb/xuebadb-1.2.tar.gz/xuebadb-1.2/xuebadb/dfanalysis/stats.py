import seaborn as sns
import matplotlib.pyplot as plt

def dfSummary(data):
    try:
        return data.describe()  #statistical summary
    except:
        print("Unable to provide a statistical summary")
        return False
        
def colBoxPlot(data):
    boxplot_inputs = []
    for col in range(0, len(data.columns)):
        try:
            floatdata = data[col].astype(float) #converting each column to float
            boxplot_inputs.append((col, floatdata))
        except ValueError as err:
            print(f"Unable to create box plot for column [{col}]. Error: [{err}]")
            
    plot_flag = False
    for data in boxplot_inputs:
        box_plot = sns.boxplot(data[1], orient = "v", linewidth = 2.5)
        box_plot.set(xlabel = f"Column [{data[0]}]", ylabel = "Values")
        plt.show()
        plot_flag = True
    return plot_flag
