import matplotlib.pyplot as plt

from sparselandtools.dictionaries import DCTDictionary, HaarDictionary

# create dictionary
dct_dictionary = DCTDictionary(8, 11)
haar_dictionary = HaarDictionary(8, 11)

# plot dictionary
plt.subplot(1, 2, 1)
plt.imshow(dct_dictionary.to_img(), cmap='gray')
plt.title('DCT-II Dictionary')
plt.axis('off')
plt.subplot(1, 2, 2)
plt.imshow(haar_dictionary.to_img(), cmap='gray')
plt.title('Haar Dictionary')
plt.axis('off')
plt.savefig('outputs/github1.pdf', bbox_inches='tight', transparent=True, pad_inches=0)
plt.show()
