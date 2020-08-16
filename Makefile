#For some odd reason both --cflags and --libs are needed. 
#If it works I'm not going to fix it. 
bin/main.out : src/main.cpp
	g++ `pkg-config --cflags glib-2.0 libgeoclue-2.0\
		--libs glib-2.0 libgeoclue-2.0` \
		src/main.cpp -o bin/main.out