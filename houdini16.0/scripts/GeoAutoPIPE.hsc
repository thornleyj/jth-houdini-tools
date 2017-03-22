set nullNamePath 	=	$arg1
set nullName 		=	`opname($arg1)`

set prefix = `arg(strreplace($nullName,"_"," "),0)`
set output = `strreplace($nullName,$prefix+"_","")`

#check for "PIPE_" prefix
if $prefix != "PIPE"
	message "Node name must be prefixed with \"PIPE_\""
	exit
	endif

#make the null orange
opcolor -c 1 0.4 1 $nullNamePath
				
set locationX = `arg(run("oplocate $nullNamePath"),1)`
set locationY = `arg(run("oplocate $nullNamePath"),2)`
	
#make and setup the merge sop
	set path = oppwd
	set objpath = $nullNamePath"/.."
	opcd $objpath
	set mergename = "IN_"$output
	set command = "hou.node('"$objpath"').createNode('object_merge').name()"
	#message $command
	set genname = `pythonexprs($command)`
	#message $genname
	opparm $genname objpath1 ( $nullNamePath )	
	oplocate -x $locationX -y `$locationY-1` $genname
	opcolor -c 0.5 0.5 0.9 $genname
	opname -u $genname $mergename
	opcd $path
	
	
