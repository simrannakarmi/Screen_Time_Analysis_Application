from actual_time import Time
import matplotlib.pyplot  as plt
import plotly.express as px
import plotly.graph_objects as go
obj=Time()
dataf=obj.total_time()
labels =dataf['name']
# print(labels)
# values = dataf['total_time']
y_data_seconds = [y.total_seconds() for y in dataf['total_time']]
values=y_data_seconds
# print(values)
plt.bar(labels, values)
# Add labels and title
plt.xlabel('Applications')
plt.ylabel('Usage in seconds')
plt.title('Screen Time Analysis')
plt.show()