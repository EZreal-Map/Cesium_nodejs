import os


def get_subdirectories(directory_path):
    subdirectories = [name for name in os.listdir(
        directory_path) if os.path.isdir(os.path.join(directory_path, name))]
    return subdirectories


def read_count_array(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        count_array = [int(line.strip()) for line in lines]
    return count_array


def create_binary_array(count_array, num):
    binary_array = [1 if count > num else 0 for count in count_array]
    return binary_array


directory_path = '../flood/30jiami'
subdirectories = get_subdirectories(directory_path)
# 按照数字大小排序
sorted_subdirectories = sorted(subdirectories, key=lambda x: int(x))

# center_file_path = os.path.join(
#     directory_path, sorted_subdirectories[0], 'center.txt')
input_file = os.path.join(
    directory_path, sorted_subdirectories[0], 'count_array.txt')

# 读取count_array.txt文件，获取原始数组
count_array = read_count_array(input_file)

# 统计大于num的个数
num = 30  # 替换为你的阈值num
count_greater_than_num = sum(1 for count in count_array if count > num)
print("大于num的个数:", count_greater_than_num)

# 创建大小相同的二进制数组，大于num的为1，小于等于num的为0
binary_array = create_binary_array(count_array, num)
# print("二进制数组:", binary_array)
