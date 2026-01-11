#Kütüphaneleri çağırıyoruz
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Verileri Yüklüyoruz
happiness_2023 = pd.read_csv('WHR_2023.csv')
un_profiles = pd.read_csv('country_profile_variables.csv')

#Verileri Temizliyoruz 
#Ülke isimlerini normalize ediyoruz strip ile boşlukları siliyoruz , lower ile küçük harfe çeviriyoruz
happiness_2023['country'] = happiness_2023['country'].str.strip().str.lower()
un_profiles['country'] = un_profiles['country'].str.strip().str.lower()

#GDP sayısal olmayan bir değer varsa eğer diye sayısal tipe çeviriyoruz eğer sayısal olmayan değer varsa nan(boş değer)olur.
gdp_col = 'GDP: Gross domestic product (million current US$)'
un_profiles[gdp_col] = pd.to_numeric(un_profiles[gdp_col], errors='coerce')

#Veri Birleştirme (Merging)
#İki veri setini 'country' anahtarı ile birleştiriyoruz
merged_df = pd.merge(happiness_2023, un_profiles, on='country', how='inner') #her iki veri setinde ortak ülkeleri alır

#şekil 1: Ekonomi vs Mutluluk 
plt.figure(figsize=(10, 6))
sns.regplot(data=merged_df, x=gdp_col, y='happiness_score', scatter_kws={'alpha':0.5})
plt.title('Ekonomik Hacim (GDP) ve Mutluluk Skoru Arasındaki İlişki', fontsize=14)
plt.xlabel('Toplam GSYH (Milyon USD)', fontsize=12)
plt.ylabel('Mutluluk Skoru', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

#Şekil 2: Bölgesel Mutluluk Ortalamaları 
plt.figure(figsize=(12, 6))
merged_df.groupby('region')['happiness_score'].mean().sort_values().plot(kind='barh', color='teal')
plt.title('Bölgelere Göre Ortalama Mutluluk Skorları', fontsize=14)
plt.xlabel('Ortalama Mutluluk Skoru')
plt.ylabel('Bölge')
plt.tight_layout()
plt.show()

#Korelasyon Katsayısı
correlation = merged_df[gdp_col].corr(merged_df['happiness_score'])
print(f"GSYH ve Mutluluk Arasındaki Korelasyon Katsayısı: {correlation:.2f}")