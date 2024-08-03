import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import exposure
from tqdm import tqdm

try: 
    from . import utils
except:
    import utils
    

def preprocess_image(image_path):
    """
    Open an image, convert it to LAB color space, split into L, a, and b channels, 
    and calculate the gradient of each channel. Then merge the gradients by taking
    the maximum value for each pixel from the three gradients.
    
    :param image_path: Path to the input image.
    """
    # Read the input image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    
    # Convert the image to LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    
    # Split the LAB image into L, a, and b channels
    L, a, b = cv2.split(lab_image)
    
    # Calculate the gradient for each channel
    grad_L = utils.calculate_gradient(L)
    grad_a = utils.calculate_gradient(a)
    grad_b = utils.calculate_gradient(b)
    
    # Merge the gradients by taking the maximum value for each pixel
    merged_gradient = np.maximum(np.maximum(grad_L, grad_a), grad_b)
    
    return(merged_gradient)
    
def calculate_hog(image, orientations=16, pixels_per_cell=(16, 16), cells_per_block=(2, 2), visualize=True):
    """
    Calculate the Histogram of Oriented Gradients (HOG) for a given image.
    
    :param image_path: Path to the input color image.
    :param orientations: Number of orientation bins.
    :param pixels_per_cell: Size (in pixels) of a cell.
    :param cells_per_block: Number of cells in each block.
    :param visualize: Whether to return an image of the HOG.
    :return: HOG feature vector and HOG image (if visualize is True).
    """
    
    # Calculate HOG features
    hog_features, hog_image = hog(image, orientations=orientations, pixels_per_cell=pixels_per_cell,
                                  cells_per_block=cells_per_block, visualize=visualize, block_norm='L2-Hys')
    
    return(hog_features, hog_image)

def bin_hog_features(hog_features, n_bins):
    """
    Bin the HOG features into n bins.
    
    :param hog_features: HOG feature vector.
    :param n_bins: Number of bins.
    :return: Binned HOG feature vector.
    """
    # Calculate the size of each bin
    bin_size = len(hog_features) // n_bins
    
    hog_features = hog_features / sum(hog_features)

    binned_hog_features = np.sum(hog_features.reshape(bin_size, n_bins), axis=0)
    
    return binned_hog_features

def plot_hog_histogram(binned_hog_features, n_bins):
    """
    Plot the histogram of the binned HOG features.
    
    :param binned_hog_features: Binned HOG feature vector.
    :param n_bins: Number of bins.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(range(n_bins), binned_hog_features, align='center', alpha=0.7)
    plt.xlabel('Bin')
    plt.ylabel('Frequency')
    plt.title('Histogram of Oriented Gradients (HOG) with 16 Bins')
    plt.show()



def getSelfSimilarity(image, nLevels=4, bins=16, methods=['ground','parent','neighbors','anisotropy']):
    
    results = {}
    
    image = cv2.resize(image, (1024, 1024), interpolation=cv2.INTER_CUBIC)
    
    # Convert the image to LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    
    # Split the LAB image into L, a, and b channels
    L, a, b = cv2.split(lab_image)
    
    # Calculate the gradient for each channel
    grad_L = utils.calculate_gradient(L)
    grad_a = utils.calculate_gradient(a)
    grad_b = utils.calculate_gradient(b)
    
    # Merge the gradients by taking the maximum value for each pixel
    merged_gradient = np.maximum(np.maximum(grad_L, grad_a), grad_b)
    # plt.imshow(merged_gradient)
    hog_features, hog_image = hog(merged_gradient, orientations=16, pixels_per_cell=(16,16),
                                  cells_per_block=(2,2), visualize=True, block_norm='L2-Hys')
    
    hists = []
    
    print('Computing Hogs. This is gonna take some time.')
    for level in tqdm(range(0, nLevels)):
        thislevel = []
        
        h, w = merged_gradient.shape
        
        hn = h // (2**level)
        wn = w // (2**level)
        
        for i in range(0, h, hn):
            for j in range(0, w, wn):
                
                partialimage = merged_gradient[i:i+hn, j:j+wn]
                 
                hog_features, hog_image = calculate_hog(partialimage, orientations=16)
                
                # Bin the HOG features into n 
                hist = bin_hog_features(hog_features, 16)
                thislevel.append(hist)
                
        hists.append(np.array(thislevel))
    
    if('ground' in methods):
        #ground 
        ground = hists[0].flatten()
        results['ground'] = np.median([(np.sum([min(ground[n], y[n]) for n in range(0, 16)])) for y in hists[3]]).astype(float)

    if('parent' in methods):
        #parent approach
        temp = []
        for i in range(0, len(hists[-2])):
            nodes = utils.find_child_nodes(i)
            temp.append(np.median([(np.sum([min(hists[2][i][n], y[n]) for n in range(0, 16)])) for y in hists[3][nodes]]))
        results['parent'] = np.median(temp).astype(float)
    
    if('neighbors' in methods):
        #neighbors 
        temp = []
        for i in range(0, len(hists[3])):
            nodes = utils.find_neighbors(i)
            temp.append(np.median([(np.sum([min(hists[3][i][n], y[n]) for n in range(0, 16)])) for y in hists[3][nodes]]))
        results['neighbors'] = np.median(temp).astype(float)
    
    if('anisotropy' in methods):
        results['anisotropy'] = np.std(hists[-1]).astype(float)
    return(results)
    
    

if __name__ == "__main__":
    
    nLevels = 4
    
    image_path = "/home/giulio/Repositories/pyaesthetics/share/data/branches.jpg"  # Replace with the path to your image file
    
    image = cv2.imread(image_path)
   
    results = getSelfSimilarity(image)
    print(results)