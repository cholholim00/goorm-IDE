import seaborn as sns
import matplotlib.pyplot as plt

# 샘플 데이터 로드 (붓꽃 데이터)
df = sns.load_dataset('iris')

# 막대그래프: 종별 평균 petal_length 비교
sns.barplot(x='species', y='petal_length', data=df)
plt.title('Species vs Petal Length')
plt.show()

# 산점도: 꽃받침 길이와 너비의 관계
sns.scatterplot(x='sepal_length', y='sepal_width', hue='species', data=df)
plt.title('Sepal Length vs Width')
plt.show()