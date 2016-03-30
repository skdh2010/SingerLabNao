
import sys
import operator
import Queue
from xml.dom import minidom
from collections import defaultdict
import os.path
import zipfile
import glob

" ------------------ process comments ------------------ "

def process_comments(comment_list):
	type_list = {}
	first_node = -1
	for comment in comment_list:
	    node_id = float(comment.attributes['node'].value)
	    node_comment = comment.attributes['content'].value

	    #add more later if wanted, now just soma
	    if node_comment == 'soma' or node_comment == 'Soma' or node_comment == 's':
	    	type_list[node_id] = 1

        #check for first node to start
	    if 'First' in node_comment or 'first' in node_comment:
	    	first_node = node_id

	return type_list, first_node

" ------------------- process nodes ------------------- "
def process_nodes(node_list):
	xyz_and_radius = {}
	for node in node_list:
	    node_id = float(node.attributes['id'].value)
	    node_x = float(node.attributes['x'].value)
	    node_y = float(node.attributes['y'].value)
	    node_z = float(node.attributes['z'].value)
	    node_radius = float(node.attributes['radius'].value)
	    inVp = float(node.attributes['inVP'].value)

	    node_radius_factor = -99
	    
	    if inVp == 0:
	    	node_radius_factor = 13.2
	    elif inVp == 1:
	    	node_radius_factor = 26
	    elif inVp == 2:
	    	node_radius_factor = 26

	    node_x = node_x * 13.2
	    node_y = node_y * 13.2
	    node_z = node_z * 26
	    node_radius = node_radius * node_radius_factor

	    if node_id not in xyz_and_radius:
	    	xyz_and_radius[node_id] = [node_id, node_x, node_y, node_z, node_radius]

	#print to debug
	#    print node_id, " - " , xyz_and_radius[node_id]
	return xyz_and_radius

" ------------------- process edges ------------------- "

def process_edges(edge_list):
	edge_hash = {}
	edge_hash = defaultdict(lambda: [], edge_hash) #key = parent, val = list of children
	
	for edge in edge_list:
		source = float(edge.attributes['source'].value)
		target = float(edge.attributes['target'].value)

		if source not in edge_hash:
			edge_hash[source] = [target]
		else:
			edge_hash[source].append(target)

		if target not in edge_hash:
			edge_hash[target] = [source]
		else:
			edge_hash[target].append(source)

	#print to debug
	# for key, val in parent_hash.items():
	# 	print key, " - ", val
	# for key, val in edge_hash.items():
	# 	print key, " - ", val
	return edge_hash

" ------------------- reorder nodes ------------------- "

def reorder_nodes(first_node, xyz_and_radius):
	rehash = {}
	parent_hash = {}
	queue = Queue.Queue() #put, get
	visited = {}
	visited = defaultdict(lambda: 0, visited)

	min_n = float("inf")
	for node in node_list:
		node_id = float(node.attributes['id'].value)
		min_n = node_id if node_id < min_n else min_n


	#default root = node with lowest id
	if first_node == -1:	
		first_node = int(min_n)
	parent_hash[first_node] = -1

	to_process = xyz_and_radius[first_node]
	queue.put(to_process)
	visited[first_node] = 1

	curr = 0
	while not queue.empty():
		to_process = queue.get()
		id_temp = to_process[0]

		curr += 1
		rehash[curr] = id_temp
		visited[id_temp] = 1

		list_to_add = edge_hash[id_temp]
		for elem in list_to_add:
			if(visited[elem] == 0):
				parent_hash[elem] = id_temp
				queue.put(xyz_and_radius[elem])

	# # print to debug
	# print 's'
	# for i in range(1, len(rehash)+1):
	# 		true_id = rehash[i]
	# 		print i, true_id
	# print 'e'
	return rehash, parent_hash

" ---------------------  write vtk --------------------- "

def create_file(out_filename, rehash, xyz_and_radius, parent_hash):

	n_new = len(rehash) #every node with parent plus root

	points_array = []
	lines_array = []

	head1 = "# vtk DataFile Version 3.0\n"
	head2 = "vtk output\n"
	head3 = "ASCII\n"
	head4 = "DATASET POLYDATA\n\n"
	head = head1 + head2 + head3 + head4

	with open(out_filename, 'w') as f:
		f.write(head)
		for i in range(1, n_new+1):
			true_id = rehash[i]
			x = xyz_and_radius[true_id][1]
			y = xyz_and_radius[true_id][2]
			z = xyz_and_radius[true_id][3]
			radius = xyz_and_radius[true_id][4]
			temp_points = [str(x), str(y), str(z)] 
			points_array.append(temp_points)
			
			p = -1
			for id_key,id_val in rehash.items():
				if id_val == parent_hash[true_id]:
					p = id_key

			temp_lines = [p, i]
			lines_array.append(temp_lines) 
		
		f.write("POINTS %d float\n" % i)
		for n in range(0, i):
			temp_points = points_array[n]
			f.write(temp_points[0] + " " + temp_points[1] + " " +  temp_points[2] + "\n")
		f.write("\n")
		f.write("LINES %d " % (i-1))
		j = (i-1) * 3
		f.write("%d\n" % j)
		for n in range(1,i):
			temp_lines = lines_array[n]
			f.write("2 " + str(temp_lines[0]-1) + " " + str(temp_lines[1]-1) + "\n")
		f.write("\n")
		f.write("VERTICES %d " % i)
		f.write("%d\n" % (i*2))
		for n in range(0, i):
			f.write("1 " + "%d\n" % n)
		

	print "FILE created >",out_filename

" ---------------------  MAIN --------------------- "

path = "c:/d/Archive/" # ex: "Desktop/Cells/"

for filename in os.listdir(path):
	if 'zip' in filename:
		zfile = zipfile.ZipFile(path+filename)
		zfile.extractall() 
		infilename = "annotation.xml"
		xmldoc = minidom.parse(infilename)	
		
		things = xmldoc.getElementsByTagName('thing')
		name = things[0].attributes['comment'].value

		# retrieve data
		node_list = xmldoc.getElementsByTagName('node')
		edge_list = xmldoc.getElementsByTagName('edge')
		comment_list = xmldoc.getElementsByTagName('comment')

		# process data
		unused, first_node = process_comments(comment_list)
		xyz_and_radius = process_nodes(node_list)
		edge_hash = process_edges(edge_list)
		rehash, parent_hash = reorder_nodes(first_node, xyz_and_radius)

		#create file
		create_file("c:/d/Archive/" + name + ".vtk", rehash, xyz_and_radius, parent_hash)

	# if 'xml' in filename:
	# 	xmldoc = minidom.parse(path + filename)	
		
	# 	things = xmldoc.getElementsByTagName('thing')
	# 	name = things[0].attributes['comment'].value

	# 	# retrieve data
	# 	node_list = xmldoc.getElementsByTagName('node')
	# 	edge_list = xmldoc.getElementsByTagName('edge')
	# 	comment_list = xmldoc.getElementsByTagName('comment')

	# 	# process data
	# 	unused, first_node = process_comments(comment_list)
	# 	xyz_and_radius = process_nodes(node_list)
	# 	edge_hash = process_edges(edge_list)
	# 	rehash, parent_hash = reorder_nodes(first_node, xyz_and_radius)

	# 	#create file
	# 	create_file("VTK/" + name + ".vtk", rehash, xyz_and_radius, parent_hash)








