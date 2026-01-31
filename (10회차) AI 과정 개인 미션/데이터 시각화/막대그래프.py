import seaborn as sns
import matplotlib.pyplot as plt

# 샘플 데이터 로드 (붓꽃 데이터)
df = sns.load_dataset('iris')

# 막대그래프: 종별 평균 petal_length 비교
sns.barplot(x='species', y='petal_length', data=df)
plt.title('Species vs Petal Length')
plt.show()

# 히스토그램: petal_length 분포
sns.histplot(df['petal_length'], bins=20, kde=True)
plt.title('Distribution of Petal Length')
plt.show()

# 박스플롯: 종별 petal_width 분포
sns.boxplot(x='species', y='petal_width', data=df)
plt.title('Species vs Petal Width')
plt.show()

# 바이올린플롯: 종별 sepal_length 분포
sns.violinplot(x='species', y='sepal_length', data=df)
plt.title('Species vs Sepal Length')
plt.show()

# 페어플롯: 모든 변수 간의 관계
sns.pairplot(df, hue='species')
plt.suptitle('Pairplot of Iris Dataset', y=1.02)
plt.show()

