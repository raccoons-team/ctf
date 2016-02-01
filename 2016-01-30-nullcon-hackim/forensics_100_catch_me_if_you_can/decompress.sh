FILE=$(file secret2)

echo $FILE

# Note: we had to download some custom Russian program extracting PPMD archives.

case "$FILE" in
	*RAR*)
		unrar secret2
		mv secret secret2
		;;
	*Zoo*)
		mv secret2 secret2.zoo
		zoo -extract secret2.zoo
		cp secret secret2
		;;
	*7-z*)
		7z e secret2
		echo ddd
		cp secret secret2
		;;
	*ARC*)
		nomarch secret2
		cp secret secret2
		;;
	*Zip*)
		unzip secret2
		cp secret secret2
		;;
	*bzip2*)
		bunzip2 secret2
		cp secret2.out secret2
		;;
	*tar*)
		tar xf secret2
		cp secret secret2
		;;
	*Cabinet*)
		cabextract secret2
		cp secret secret2
		;;
	*XZ*)
		mv secret2 secret2.xz
		unxz secret2.xz
		;;
	*KGB*)
		kgb secret2
		mv secret secret2
		;;
	*ARJ*)
		mv secret2 secret2.arj
		arj e secret2.arj
		mv secret secret2
		;;
	*PPMD*)
		wine PPMd.exe d secret2
		mv secret secret2
		;;
	*rzip*)
		mv secret2 secret2.rz
		rzip -d secret2.rz
		;;
	*gzip*)
		mv secret2 secret2.gz
		gunzip secret2.gz
		;;
esac

rm secret
