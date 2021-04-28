def filter() :
	print('called filter function in filter_packets.py')
	builtLine = ""
	num = 0
	for filenum in range(1, 5) : #Its 5 because if its 4 it doesnt read pcap 4
		f = open("./Captures/Node" + str(filenum) + ".txt", 'r')
		fnew = open("./Captures/Node" + str(filenum) + "Filtered.txt", 'w')
		lines = f.readlines()
		for line in lines:
			temp = line
			if "No." in temp :
				x = "ICMP" in builtLine and "unreachable" not in builtLine
				if x == True :
					fnew.write(builtLine)
				shouldBuild = True
				builtLine = ""
			if shouldBuild == True :
				builtLine = builtLine + temp
				num = num + 1
		f.close()
		fnew.close()
		print("Node" + str(filenum) + " filtered.")

	print("Packet captures filtered for ICMP requests")
