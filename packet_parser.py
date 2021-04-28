def parse() :
	print('called parse function in packet_parser.py')
	parsed =  [[], [], [], []]
	curline = 0
	for filenum in range(1, 5) :
		f = open("./Captures/Node" + str(filenum) + "Filtered.txt", 'r')
		lines = f.readlines()
		for line in lines :
			curline = curline + 1
			if curline == 2 :
				lineList = line.split()			
				# Format                   Source IP  Destination IP  Packet Size  Type         Time            TTL
				parsed[filenum-1].append([lineList[2], lineList[3], lineList[5], lineList[8], lineList[1], lineList[11]])
			if "No." in line :
				curline = 1
			
		print("Node" + str(filenum) + " parsed.")
	print("Filtered packet captures parsed")
	return(parsed)
	
