#Simple 2D Convolution implementation from scratch in Python 
# Assumes single-channel input/output for simplicity; extend for multi-channel 
def conv2d(input_matrix, kernel, stride=1, padding=1, bias=0): 
    """     Performs 2D convolution on a single-channel input matrix.    
 :param input_matrix: List of lists (2D matrix, height x width)     :param kernel: List of lists (2D kernel, k_h x k_w)     :param stride: Integer step size     :param padding: Integer padding size (symmetric)     :param bias: Float bias to add to each output element     :return: Output matrix as list of lists     """    
    # Get dimensions  
    height_in = len(input_matrix)  
    width_in = len(input_matrix[0]) if height_in > 0 else 0  
    k_h = len(kernel)  
    k_w = len(kernel[0]) if k_h > 0 else 0          # Calculate output dimensions
    height_out = (height_in - k_h + 2 * padding) // stride + 1
    print(f'{height_in} {k_h} {padding} {stride}')
    print(height_out)
    width_out = (width_in - k_w + 2 * padding) // stride  + 1        
    print(width_out)
 # Create padded input
    padded_height = height_in + 2 * padding
    padded_width = width_in + 2 * padding
    padded_matrix = [[0 for _ in range(padded_width)] for _ in range(padded_height)]     
    for i in range(height_in):         
        for j in range(width_in):             
            padded_matrix[i + padding][j + padding] = input_matrix[i][j]          
    # Initialize output     
    output = [[0 for _ in range(width_out)] for _ in range(height_out)]  
    # Perform convolution     
    for i in range(height_out):         
        for j in range(width_out):             
            sum_val = 0             
            for m in range(k_h):                 
                for n in range(k_w):                     
                    # Get input value from padded matrix                     
                    input_val = padded_matrix[i * stride + m][j * stride + n]                     
                    kernel_val = kernel[m][n]                     
                    sum_val += input_val * kernel_val
            output[i][j] = sum_val + bias          
    return output  
# Example usage 
if __name__ == "__main__":     
    # Input 5x5 matrix     
    values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -111, 48, -64, 20, -116, -121, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 109, 31, 31, 31, 31, -25, 104, 104, 104, 104, 104, 104, 104, 104, -115, -32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -125, -41, 14, -41, -105, -7, 31, -114, 31, 31, 31, 73, 100, 31, 31, 71, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, -51, -19, -125, -125, -125, -42, -28, 91, 31, 43, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -37, 105, 53, -61, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -103, 58, -44, -37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 122, 31, -58, 51, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -42, -109, 31, -9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 31, -100, -117, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 97, 95, -35, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90, 31, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, -2, 49, 107, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 121, -72, 31, -73, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, -12, 31, 77, -47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -14, 31, 31, -102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -5, -40, 31, -115, -75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 31, 31, -32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65, -100, 31, 31, -32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -50, 31, 31, 77, 93, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -50, 31, -54, -61, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    input_matrix = [values[i*28:(i+1)*28] for i in range(28)]
       
    # Kernel 3x3     
    kernel = [         
        [106, 111, 6],         
        [19, 64, 117],         
        [-128,-50 , 85]     
    ]          
    # Compute convolution     
    output = conv2d(input_matrix, kernel, stride=1, padding=1, bias=0)          
    # Print output     
    print("Output:")     
    for row in output:         
        print(row)     # Expected: [[-2, -2, -2], [-2, -2, -2], [-2, -2, -2]]