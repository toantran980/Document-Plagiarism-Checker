# Sorting: Organize files by author, title, or date using Merge Sort

# Function to sort files by a specific key (author, title, or date)
def mergeSort(files, key):
        
    if len(files) > 1:
        mid = len(files) // 2  # Find the middle index
        left_half = files[:mid]  # Divide list into two halves
        right_half = files[mid:]

        # Recursively sort both halves
        mergeSort(left_half, key)
        mergeSort(right_half, key)

        # Merge the sorted halves
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][key] < right_half[j][key]:
                files[k] = left_half[i]
                i += 1
            else:
                files[k] = right_half[j]
                j += 1
            k += 1

        # Copy any remaining elements from the left half
        while i < len(left_half):
            files[k] = left_half[i]
            i += 1
            k += 1

        # Copy any remaining elements from the right half
        while j < len(right_half):
            files[k] = right_half[j]
            j += 1
            k += 1

