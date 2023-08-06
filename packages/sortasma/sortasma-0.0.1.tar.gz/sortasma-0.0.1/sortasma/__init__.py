
# coding: utf-8

# In[3]:


import timeit
start = timeit.default_timer()

def parent(i): 
    return (i-1) // 2

def leftChild(i):
    return 2*i + 1

def rightChild(i):
    return 2*i + 2

#The previous three fucntions are used to convert the array input by the user into a heap structure.
# PRECONDITION: arr stores a heap, but the first element can be wrong
def heapify(slist, p): #define the fucntion heapify which converts the array to heap,
#where the parameters are the input fucntion.
#P is the smallest value in the heap tree 
    if p >= len(slist):
        return
    l = leftChild(p)#Define the first childnode to the left.
    r = rightChild(p)#Define the second childnode to the right.
    smallest = p#The parent is the smallest value at the top of the heap tree.
    if l < len(slist) and slist[l] < slist[smallest]: 
        smallest = l
    if r < len(slist) and slist[r] < slist[smallest]:
        smallest = r
    swap(slist, p, smallest) #use the fucntion swap to move the smallest node to its position.
    if smallest != p:
        heapify(slist, smallest)
    return 

def swap(slist, i, j):
    slist[i], slist[j] = slist[j], slist[i] 
    #Use the technique of bubble sort to swap the elements within the heap tree.

def makeHeap(slist): #Define the fucntion used to convert the input array into a heap tree.
    for i in reversed(range(len(slist) // 2)):
        heapify(slist, i)

def heapSort(slist):
    res = []
    # we have to make arr into a heap
    makeHeap(slist)
    while slist: #While the array is not empty
        res.append(slist[0])#Add the value of the index number 0 to the result
        slist[0] = slist[-1] # put the last elem in index 0
        slist.pop() 
        heapify(slist, 0)
    return res

def kMergeSort(slist, k):
    k = min(k, len(slist))
    if len(slist) <= 1: #Don't slice the array if its length is less than or equal to one.
        return slist
    # Divide the array into k segments each with m elements
    m = len(slist) // k   # length of the sub-array
    segments = [] #Make an empty list to store segements.
    for i in range(k):
        # look at segment nr i
        # what would be segment nr 0 ? -> arr[b, b + m]
        # what would be segment nr 1 ? -> arr[b + m, b + 2m] 
        segB = i*m
        segE = (i+1)*m if i < k - 1 else len(slist)
        seg = slist[segB:segE]
        # sort that segment and put it in segments
        segments.append(kMergeSort(seg, k)) #Add the sorted segments into the current ones
    slist = kNormalMerge(segments) #Update the existing array with the sorted segments.
    return slist
def kmerge_asma(slist,k):
    print("K-way merge sorted array is",kMergeSort(slist,k),"Run time in seconds:",Time)#print the final sorted array.

    
def kMerge(segments, k):
    res = [] #start with empty set of the result
    heap = [] #Add a list where the heap tree is formed into an array. 
    for i in range(k):
        if not segments[i]:
            continue
        heap.append( (segments[i][0], i) )
        segments[i].pop(0)
    makeHeap(heap)
    while heap: #Run the loop whenever there is anything in the list.
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
    for each in segments: #For each of the sliced arrays do the following.
        i = 0
        while len(each) > 0:
#While there are items in each of the segments, do the following:
            if (each[0] <= res[0]): 
#Compare the fist item in the sliced arrays with the first iten in the final array.
                res.insert(0, each.pop(0))
#If the sliced array has the smallest item, remove that item to the final array.
#additionally, remove the item from the sliced array, so it compares the second item, 
#which is now had index 0.
            else: 
#If the segement doesn't have the smallest value,add one to the counter. 
                i += 1
                if (i == len(res)) or (each[0] <= res[i]):
                    res.insert(i, each.pop(0))
    return(res)
#Take the input from the user and convert it into a list.
stop = timeit.default_timer()
Time = stop - start


# In[6]:


import timeit
start = timeit.default_timer()
def mergesort_asmaa(slist):
    if len(alist)>1:
        mid = len(slist)//2
        lefthalf = slist[:mid]
        righthalf = slist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                slist[k]=lefthalf[i]
                i=i+1
            else:
                slist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            slist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            slist[k]=righthalf[j]
            j=j+1
            k=k+1
    return(slist)
stop = timeit.default_timer()
Time = stop - start


# In[8]:


import timeit
start = timeit.default_timer()
def shellSort_asmaa(slist):
    sublistcount = len(slist)//2
    while sublistcount > 0:

      for startposition in range(sublistcount):
        gapInsertionSort(slist,startposition,sublistcount)

      

      sublistcount = sublistcount // 2
    return(slist)

def gapInsertionSort(slist,start,gap):
    for i in range(start+gap,len(slist),gap):

        currentvalue = slist[i]
        position = i

        while position>=gap and slist[position-gap]>currentvalue:
            slist[position]=slist[position-gap]
            position = position-gap

        slist[position]=currentvalue
def shellsort_asmaa(slist,k):
    print("The shell sorted array is",shellsort_asmaa(slist),"Run time in seconds:",Time)#print the final sorted array.
stop = timeit.default_timer()
Time = stop - start

