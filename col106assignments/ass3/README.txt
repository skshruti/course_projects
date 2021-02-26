Shruti Kumari 2018CS50420
README file:

Class Pair:

toString() method: It returns concatened first name and last name. the return type is String.


Class Student: 

pair() method: It returns the first name and last name corresponding to the student object which works as a key. the return type is Pair<String, String>.

getData() method: It returns all the data of the student in a single line. the return type is String.

fname() method: It returns the first name of the studen. the return type is String.

lname() method: It returns the last name of the studen. the return type is String.

hostel() method: It returns the hostel of the student. the return type is String.

department() method: It returns the department of the student. the return type is String.

cgpa() method: It returns the cgpa of the student. the return type is String.


Class DoubleHashing_<K, T> method:

h(K key,int i) method:It calculates and returns the index by using the functions given in the assignment. The return type is long.

insert(K key, T obj) method: It returns the number of times a new h is calculated. The return type is integer. It first calculates an h and if the element in the array corresponding to that value of h is not empty, a new value of h is calculated till an empty array[h] is found. when an empty array[h] is found finally, the obj is stored there. The return type is integer. The best case time complexity is O(1) and the worst case is O(n).

update(K key, T obj) method:It returns the number of times a new h is calculated.The return type is integer. It first calculates an h and if the value of key corresponding to the obj stored in the array[h] is not equal to the key, a new value of h is calculated till an array[h] is found whose key equals the the value of key which is given as an input and then the obj is updated there. The return type is integer. The best case time complexity is O(1) and the worst case is O(n).

delete(K key) method: It returns the number of times a new h is calculated. The return type is integer. It first calculates an h and if the value of key corresponding to the obj stored in the array[h] is not equal to the key, a new value of h is calculated till an array[h] is found whose key equals the the value of key which is given as the input and then the obj is deleted there. The best case time complexity is O(1) and the worst case is O(n). 

contains(K key) method: It checks if the hashTable contains any object which corresponds to the key or not. The return type is boolean. It checks if the first array[h] contains the object which corresponds to the key or not. If yes, true is returned. if not, a while loop is run till the index reaches its initial value and the key stored in each array[h] is compared to the key which is given as the input. If no case matches, false is returned. The best case time complexity is O(1) and the worst case is O(n).

get(K key) method: It returns the obj corresponding to the key given in a single line. It uses the method getData() of the class Student. The return type is String. It first calculates an h and if the value of key corresponding to the obj stored in the array[h] is not equal to the key, a new value of h is calculated till an array[h] is found whose key equals the the value of key which is given as an input and then the data stored in that array[h] is extracted and executed in the form of a String. The best case time complexity is O(1) and the worst case is O(n).

address(K key) method: It returns the string representation of the index where the object for the given key was finally inserted. It first calculates an h and if the value of key corresponding to the obj stored in the array[h] is not equal to the key, a new value of h is calculated till an array[h] is found whose key equals the the value of key which is given as an input and then the final index is returned after being converted to a string. The best case time complexity is O(1) and the worst case is O(n).


Class bst:

insertbst(Student obj) method: It checks if the first node is null or not. If yes, the obj is inserted there. if not, the first name of Student object stored in the node is compared to the first name of obj. If it is greater than obj, the function is repeated for the binary tree considering the right node of this node as the root. If not,the function is repeated for the binary tree considering the left node of this node as the root. the recursion is continued till an empty node is found and the obj is inserted there. The return type is integer and it returns the number of nodes touched. The average case time complexity is O(log n) and the worst case is O(n).

updatebst(Student obj) method: It compares the pair of the object stored in the first node with the pair of the object stored in the node initially. If equal, the object previously stored is replaced by obj. if not, the first name of Student object stored in the node is compared to the first name of obj. If it is greater than obj, the function is repeated for the binary tree considering the right node of this node as the root. If not,the function is repeated for the binary tree considering the left node of this node as the root. the recursion is continued till an empty node is found and the obj is updated there. The return type is integer and it returns the number of nodes touched. The average case time complexity is O(log n) and the worst case is O(n).

deletebst(Pair pair) method: the first name of the object stored in the root node is compared to key.first. if they are equal, four cases arise: either the lest and right of the node are both null, here simply the node is deleted. if one of the left or right are null, the data stored in the node is changed to the data stored in left or right and both left and right are left null finally. if both are not null a pointer minbst is created which traverses once right and then left till it reaches a null node. then the data stored in the root node is changed to minbst.data and the last node to which minbst pointed is changed to null. and if the first name of the object stored in the root of the bst stored in the array[h] is not equal to key.first, accordingly this.left.deletebst(pair) or this.right.deletebst(pair) is executed. 
containsbst(String key) method: It compares the concatened first name and and last name of the object stored in the first node to the key. If equal, the function returns true. if not, two cases arise: If it is greater than obj, the function is repeated for the binary tree considering the right node of this node as the root. If not,the function is repeated for the binary tree considering the left node of this node as the root. the recursion is continued till the compared objects become equal or we reach a null node. The return type is boolean and it returns if we ever reach a node where the compared objects become equal or not. The average case time complexity is O(log n) and the worst case is O(n).

getbst(String key) method: It compares the concatened first name and and last name of the object stored in the first node to the key. If equal, the function returns data of the object stored in the node using the getData() function. if not, two cases arise: If it is greater than obj, the function is repeated for the binary tree considering the right node of this node as the root. If not,the function is repeated for the binary tree considering the left node of this node as the root. the recursion is continued till the compared objects become equal and then the data of the object stored in the node using the getData() function. The return type is String. The average case time complexity is O(log n) and the worst case is O(n).

addressbst(String key) method: It compares the concatened first name and and last name of the object stored in the first node to the key. If equal, the function returns " ". if not, two cases arise: If it is greater than obj, R is added to the String which is to be returned plus the function is repeated for the binary tree considering the right node of this node as the root. If not, L is added to the String which is to be returned plus the function is repeated for the binary tree considering the left node of this node as the root. the recursion is continued till the compared objects become equal or we reach a null node. The return type is String. The average case time complexity is O(log n) and the worst case is O(n).

Class SeparateChaining_<K, T>:

h(K key) method: It calculates and returns the index by using the functions given in the assignment. The return type is long.

insert(K key, T obj) method: index is calculated using the h function. if the array[h] is null, obj is inserted there. if not array[h].insertbst((Student) obj) is executed.

update(K key, T obj) method: index is calculated using the h function. if the key corresponding to the object stored in the array[h] is equal to key, obj is updated there. if not array[h].updatebst((Student) obj) is executed.

delete(K key) method: index is calculated using the h function. the first name of the object stored in the root of the bst stored in the array[h] is compared to key.first. if they are equal, four cases arise: either the lest and right of the node are both null, here simply the node is deleted. if one of the left or right are null, the data stored in the node is changed to the data stored in left or right and both left and right are left null finally. if both are not null a pointer minbst is created which traverses once right and then left till it reaches a null node. then the data stored in the root node is changed to minbst.data and the last node to which minbst pointed is changed to null. and if the first name of the object stored in the root of the bst stored in the array[h] is not equal to key.first, accordingly array[h].deletebst is executed.

contains(K key) method: index is calculated using the h function. then the array[h].containsbst(key.toString()) is executed.

get(K key) method: index is calculated using the h function. then the array[h].getbst(key.toString()) is executed.

address(K key) method: index is calculated using the h function. then index+"-"+array[h].addressbst(key.toString()) is returned.

Class Assignment3: 

The file is read using buffered reader and file reader and equating args[1] with DH or SCBST, accordingly hashTable of the required type is created and using the if else commands, it is decided which method is to be executed by storing the data in an array named tokens and comparing its first value to insert, delete etc.


