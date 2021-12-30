import os
import tempfile
import heapq
import sys


class heapnode:
    def __init__(
            self,
            item,
            fileHandler,
    ):
        self.item = item
        self.fileHandler = fileHandler


class externamMergeSort:
    def __init__(self):
        self.sortedTempFileHandlerList = []
        self.getCurrentDir()

    def getCurrentDir(self):
        self.cwd = os.getcwd()

    def heapify(
            self,
            arr,
            i,
            n,
    ):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left].item > arr[i].item:
            biggest = left
        else:
            biggest = i

        if right < n and arr[right].item > arr[biggest].item:
            biggest = right

        if i != biggest:
            (arr[i], arr[biggest]) = (arr[biggest], arr[i])
            self.heapify(arr, biggest, n)

    def construct_heap(self, arr):
        l = len(arr) - 1
        mid = l // 2 + 1
        while mid >= 0:
            self.heapify(arr, mid, l)
            mid -= 1

    def mergeSortedtempFiles_low_level(self):
        list = []
        sorted_output = []
        for tempFileHandler in self.sortedTempFileHandlerList:
            item = int(tempFileHandler.readline().strip())
            list.append(heapnode(item, tempFileHandler))
        
        

        self.construct_heap(list)
        while True:
            max = list[0]
            if max.item == -sys.maxsize:
                break
            sorted_output.append(max.item)
            fileHandler = max.fileHandler
            item = fileHandler.readline().strip()
            if not item:
                item = -sys.maxsize
            else:
                item = int(item)
            list[0] = heapnode(item, fileHandler)
            self.heapify(list, 0, len(list))
        return sorted_output

    def splitFiles(self, largeFileName, smallFileSize):
        largeFileHandler = open(largeFileName)
        tempBuffer = []
        size = 0
        while True:
            number = largeFileHandler.readline()
            if not number:
                break
            tempBuffer.append(number)
            size += 1
            if size % smallFileSize == 0:
                tempBuffer = sorted(tempBuffer, key=lambda no: \
                    int(no.strip()), reverse=True)
                print(len(tempBuffer), tempBuffer)
                tempFile = tempfile.NamedTemporaryFile(dir=self.cwd
                                                           + '/temp', delete=False, mode= 'r+')
                tempFile.writelines(tempBuffer)
                tempFile.seek(0)
                self.sortedTempFileHandlerList.append(tempFile)
                tempBuffer = []
        if(len(tempBuffer) > 0):
          tempBuffer = sorted(tempBuffer, key=lambda no: \
                    int(no.strip()))
          print(len(tempBuffer), tempBuffer)
          tempFile = tempfile.NamedTemporaryFile(dir=self.cwd
                                          + '/temp', delete=False, mode= 'r+')
          tempFile.writelines(tempBuffer)
          tempFile.seek(0)
          self.sortedTempFileHandlerList.append(tempFile)



if __name__ == '__main__':
    largeFileName = 'largefile.txt'
    smallFileSize = 10000
    obj = externamMergeSort()
    obj.splitFiles(largeFileName, smallFileSize)
    
    sortedList = obj.mergeSortedtempFiles_low_level()
    print (sortedList)
    print(len(sortedList))
    """Pythonic way - Uses a generator """