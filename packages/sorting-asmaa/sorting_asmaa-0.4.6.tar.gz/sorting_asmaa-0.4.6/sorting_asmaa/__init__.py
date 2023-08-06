import timeit
import math
import timeit  # import timeit library to calculate time
start = timeit.default_timer()


def parent(i):
    return (i - 1) // 2


def leftChild(i):
    return 2 * i + 1


def rightChild(i):
    return 2 * i + 2

# The previous three fucntions are used to convert the array input by the user into a heap structure.
# PRECONDITION: arr stores a heap, but the first element can be wrong


def heapify(slist, p):  # define the fucntion heapify which converts the array to heap,
    # where the parameters are the input fucntion.
    # P is the smallest value in the heap tree
    if p >= len(slist):
        return
    l = leftChild(p)  # Define the first childnode to the left.
    r = rightChild(p)  # Define the second childnode to the right.
    # The parent is the smallest value at the top of the heap tree.
    smallest = p
    if l < len(slist) and slist[l] < slist[smallest]:
        smallest = l
    if r < len(slist) and slist[r] < slist[smallest]:
        smallest = r
    # use the fucntion swap to move the smallest node to its position.
    swap(slist, p, smallest)
    if smallest != p:
        heapify(slist, smallest)
    return


def swap(slist, i, j):
    slist[i], slist[j] = slist[j], slist[i]
    # Use the technique of bubble sort to swap the elements within the heap
    # tree.


# Define the fucntion used to convert the input array into a heap tree.
def makeHeap(slist):
    for i in reversed(range(len(slist) // 2)):
        heapify(slist, i)


def heapSort(slist):
    res = []
    # we have to make arr into a heap
    makeHeap(slist)
    while slist:  # While the array is not empty
        # Add the value of the index number 0 to the result
        res.append(slist[0])
        slist[0] = slist[-1]  # put the last elem in index 0
        slist.pop()
        heapify(slist, 0)
    return res


def kMergeSort(slist, k):
    k = min(k, len(slist))
    # Don't slice the array if its length is less than or equal to one.
    if len(slist) <= 1:
        return slist
    # Divide the array into k segments each with m elements
    m = len(slist) // k   # length of the sub-array
    segments = []  # Make an empty list to store segements.
    for i in range(k):
        # look at segment nr i
        # what would be segment nr 0 ? -> arr[b, b + m]
        # what would be segment nr 1 ? -> arr[b + m, b + 2m]
        segB = i * m
        segE = (i + 1) * m if i < k - 1 else len(slist)
        seg = slist[segB:segE]
        # sort that segment and put it in segments
        # Add the sorted segments into the current ones
        segments.append(kMergeSort(seg, k))
    # Update the existing array with the sorted segments.
    slist = kNormalMerge(segments)
    return slist


def kmerge_asmaa(slist, k):
    # print the final sorted array.
    print(
        "K-way merge sorted array is",
        kMergeSort(
            slist,
            k),
        "Run time in seconds:")
    return Time


def kMerge(segments, k):
    res = []  # start with empty set of the result
    heap = []  # Add a list where the heap tree is formed into an array.
    for i in range(k):
        if not segments[i]:
            continue
        heap.append((segments[i][0], i))
        segments[i].pop(0)
    makeHeap(heap)
    while heap:  # Run the loop whenever there is anything in the list.
        minVal = heap[0][0]
        minInd = heap[0][1]
        res.append(minVal)
        if segments[minInd]:
            # if there is a next elemnt in that segment
            # we can put it in the heap
            heap[0] = (segments[minInd][0], minInd)
            segments[minInd].pop(0)
            heapify(heap, 0)
        else:
            # there is no next elem in that segment
            heap[0] = heap[-1]
            heap.pop()
            heapify(heap, 0)
    return res


def kNormalMerge(segments):
    res = segments.pop(0)
    for each in segments:  # For each of the sliced arrays do the following.
        i = 0
        while len(each) > 0:
            # While there are items in each of the segments, do the following:
            if (each[0] <= res[0]):
                # Compare the fist item in the sliced arrays with the first
                # iten in the final array.
                res.insert(0, each.pop(0))
# If the sliced array has the smallest item, remove that item to the final array.
# additionally, remove the item from the sliced array, so it compares the second item,
# which is now had index 0.
            else:
                # If the segement doesn't have the smallest value,add one to
                # the counter.
                i += 1
                if (i == len(res)) or (each[0] <= res[i]):
                    res.insert(i, each.pop(0))
    return(res)


# Take the input from the user and convert it into a list.
stop = timeit.default_timer()
Time = stop - start


# import the time library
start = timeit.default_timer()
# define the shell sort method


def shellSort_asmaa(slist):
    sublistcount = len(slist) // 2
    while sublistcount > 0:
        for startposition in range(sublistcount):
            # call the insertion sort to sort the buckets
            gapInsertionSort(slist, startposition, sublistcount)
        sublistcount = sublistcount // 2
        # split the the gaps again
    return(slist)

# shell sorts uses insertion sort to sort the gaps
# for each iteration


def gapInsertionSort(slist, start, gap):
    for i in range(start + gap, len(slist), gap):
        currentvalue = slist[i]
        position = i
# swap the elements within the gaps to sort them
        while position >= gap and slist[position - gap] > currentvalue:
            slist[position] = slist[position - gap]
            position = position - gap
# return the posiition of the point to
# move to the other gaps.
        slist[position] = currentvalue


stop = timeit.default_timer()
Time = stop - start


def shellsort_asmaa(slist):
    # print the final sorted array.
    print(
        "The sorted array is",
        shellSort_asmaa(slist),
        "Run time in seconds:")
    return Time


# In[44]:


# define a function bucket_sort that takes a slist as parameter.
def bucket_sort(slist):
    # Inside the function set largest to the maximum element in the list and
    # set length equal to the length of the input.

    largest = max(slist)
    length = len(slist)
# Set size = largest/length.

    size = largest / length
# Create a list of empty lists and assign it to buckets.

    buckets = [[] for _ in range(length)]
# start a loop with loop variable i that iterates from 0 to the length of the list – 1.
# In each iteration, determine to which bucket slist[i] belongs.
# I have done this by taking the floor of slist[i]/size and using the
# answer as the index of the bucket.

    for i in range(length):
        j = int(slist[i] / size)
        if j != length:
            buckets[j].append(slist[i])
        else:
            # If the answer equals length, then slist[i] is placed in the last bucket,
            # that is bucket[length -1 ].
            buckets[length - 1].append(slist[i])

    for i in range(length):
        insertion_sort(buckets[i])

    result = []
    for i in range(length):
        result = result + buckets[i]
    return result
# To sort each bucket, any algorithm can be used. I have chosen
# insertion as it is effcient for small inputs.
# Perform insertion sort on each bucket.
# Concatenate the buckets to create the sorted list and return it.
# Create a function insertion_sort that takes a list as argument.


def insertion_sort(slist):
    # Inside the function create a loop with a loop variable i that counts
    # from 1 to the length of the list – 1.
    for i in range(1, len(slist)):
        # Set temp equal to the element at index i.
        temp = slist[i]
# Set j equal to i – 1.
        j = i - 1
# Create a while loop that runs as long as j is non-negative and temp is
# smaller than the element at index j.
        while (j >= 0 and temp < slist[j]):
            # Inside the while loop, set the element at index j + 1 equal to the element at index j and decrement j.
            # After the while loop finishes, set the element at index j + 1
            # equal to temp.
            slist[j + 1] = slist[j]
            j = j - 1
        slist[j + 1] = temp


# calculate the run time.
stop = timeit.default_timer()
Time = stop - start


def bucketsort_asmaa(slist):
    # print the final sorted array.
    print("The sorted array is", bucket_sort(slist), "Run time in seconds:")
    return Time


# In[62]:
start = timeit.default_timer()
# define the radix fucntion that accepts lists as an argument.


def radixsort(slist):
    # set the intial parameters
    digit = 1
    End = False
    k = 10  # The base of the numbers we choose to sort

    while not End:
        # Only remains true if we are calculating for the highest significant
        # digit.
        End = True

        # Initialize the bins which are a series of lists
        # these bins store the close inputs together to perform count sort
        bins = [list() for _ in range(k)]

        # Place items inside toBeSorted buffer into their respective bins
        for i in slist:
            temp = i // digit
            bins[temp % k].append(i)
            if temp > 0:
                End = False

        # Put the items in the bins back into the toBeSorted buffer
        toBeSortedIndex = 0
        for i in range(k):  # Goes through each bin
            bin = bins[i]
            for j in bin:  # Goes through each element in a given bin
                slist[toBeSortedIndex] = j
                toBeSortedIndex = toBeSortedIndex + 1
# Increment to sort by the next digit
        digit = digit * k
# return the sorted array
    return slist


def radixsort_asmaa(slist):
    # print the final sorted array.
    print("The sorted array is", radixsort(slist), "Run time in seconds:")
    return Time


end = timeit.default_timer()
Time = end - start


# import math and time libraries
start = timeit.default_timer()
start = timeit.default_timer()
# define the function introsort
# d is the depth of the partation


def introSort(slist, d):
    n = len(slist)
# n is the length of the liist
    if n <= 1:
        # if the list empty, return nothing
        return
    elif d == 0:
        # if the depth of the partition is zero, use heapsort
        heapSort(slist)
    else:
        # Otherwise, split the list into smaller partitions, like quicksort where p is the
        # pivot
        p = partition(slist)
        a1 = slist[:p]
        a2 = slist[p + 1:n]
# keep splitting by making new partitions
        introSort(a1, d - 1)
        introSort(a2, d - 1)
# fill the list with the new partition and remove the rest of the elements.
        for i in range(0, len(a1)):
            slist.insert(i, a1[i])
            slist.pop(i + 1)
# fill the list with the new partition and remove the rest of the elements.
        for i in range(0, len(a2) - 1):
            slist.insert(i + p + 1, a2[i])
            slist.pop(i + p + 2)
# retrun the new list
    return slist
# instead of using heapq, I coded the following
# define heap sort function


def heapSort(slist):
    END = len(slist)
# END is the length of the list
    for k in range(int(math.floor(END / 2)) - 1, -1, -1):
        heapify(slist, END, k)

    for k in range(END, 1, -1):
        swap(slist, 0, k - 1)
        heapify(slist, k - 1, 0)
# the partation fucntion that returns the new pivot to split the array.


def partition(slist):
    hi = len(slist) - 1
    x = slist[hi]
    i = 0
    for j in range(0, hi - 1):
        if slist[j] <= x:
            swap(slist, i, j)
            i = i + 1
    swap(slist, i, hi)
    return i
# define the swap function to move the elements around in the heap


def swap(slist, i, j):
    tmp = slist[i]
    slist[i] = slist[j]
    slist[j] = tmp
# define heapify fucntion that


def heapify(slist, iEnd, iRoot):
    # define the indeces for the parent node and its children
    # the following conditions are made to check whether the tree is right or not
    # if there are any mistakes in arranging the elements, the condition
    # corrects them. All of the following conditions are based on fundemental properties
    # of heap data structure.
    iL = 2 * iRoot + 1
    iR = 2 * iRoot + 2
    if iR < iEnd:
        if (slist[iRoot] >= slist[iL] and slist[iRoot] >= slist[iR]):
            return

        else:
            if(slist[iL] > slist[iR]):
                j = iL
            else:
                j = iR
            swap(slist, iRoot, j)
            heapify(slist, iEnd, j)
    elif iL < iEnd:
        if (slist[iRoot] >= slist[iL]):
            return
        else:
            swap(slist, iRoot, iL)
            heapify(slist, iEnd, iL)
    else:
        return


def introsort_asmaa(slist):
    # print the final sorted array.
    print("The sorted array is", introSort(slist, 2), "Run time in seconds:")
    return Time


end = timeit.default_timer()
Time = end - start
