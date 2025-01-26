
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
data = pd.read_csv('./data/country_adeptness.csv')

fontsize=15
#排序
data = data.sort_values(by='Adeptness',ascending=False)
#去除Adeptness为1的极端值
data = data[data['Adeptness']!=1]
#去除苏联
data = data[data['NOC']!='SUI']
#取前20
data = data.head(20)
colors=['#e45756','#f58518','#f2cf5b','#54a24b'
        ,'#439894','#4c78a8','#b279a2','#d6a5c9',
        '#9ecae9','#83bcb6','#ffbf79',
        '#d8b5a5','#ff9d98','#bab0ac'
        ]

noc_to_image = {
    "GBR": "gbr.png",
    "USA": "usa.png",
    "CAN": "canada.png",
    "GER": "germany2.png",
    "CHN": "china.png",
    "JPN": "japan.png",
    "AUS": "australia.png"
}
flag_folder = './flags/'
#绘制柱状图，展现某一国家某一项目的优势程度排名。左侧坐标显示优势程度，下方坐标显示国家名称
print(data['NOC'].unique())
plt.figure(figsize=(10, 6))
#plt.barh(data['NOC']+"-"+data['Sport'], data['Adeptness'], alpha=0.8)
#颜色依次轮流选取colors中的颜色

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
for i in range(len(data)):
    plt.barh(data['NOC'].iloc[i]+"-"+data['Sport'].iloc[i], data['Adeptness'].iloc[i], color=colors[i%len(colors)])
    #保留两位小数
    plt.text(data['Adeptness'].iloc[i]/7*6,i-0.3,str(round(data['Adeptness'].iloc[i],2)),ha='center',va='bottom',fontsize=fontsize-3,fontweight='bold')
    plt.text(data['Adeptness'].iloc[i]/2,i-0.3,data['Sport'].iloc[i],ha='center',va='bottom',fontsize=fontsize-3,fontweight='bold')
    flag = mpimg.imread(flag_folder+noc_to_image[data['NOC'].iloc[i]])
    imagebox = OffsetImage(flag, zoom=0.04)
    ab = AnnotationBbox(imagebox, (data['Adeptness'].iloc[i], i),frameon=False)
    plt.gca().add_artist(ab)


from PIL import Image
icon = Image.open('./icons/lacrosse.png')
icon = icon.resize((200, 200))
icon = np.array(icon)

plt.figimage(icon, 1700, 430, zorder=2)
#在图中添加图片
icon2=Image.open('./icons/table-tennis.png')
icon2 = icon2.resize((200, 200))
icon2 = np.array(icon2)
plt.figimage(icon2, 1200, 800, zorder=2)

#在图中添加图片
icon2=Image.open('./icons/cricket-player-with-bat.png')
icon2 = icon2.resize((200, 200))
icon2 = np.array(icon2)
plt.figimage(icon2, 1400, 600, zorder=2)
icon2=Image.open('./logo.png')
icon2 = np.array(icon2)
plt.figimage(icon2, 1800, 900, zorder=2)


plt.yticks(rotation=30)
plt.gca().set_facecolor('#f0f0f0')
plt.grid(alpha=0.9,axis='x')
#times new roman
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False
plt.xlabel('Adeptness',fontsize=fontsize)
plt.ylabel('Country',fontsize=fontsize)
plt.show()