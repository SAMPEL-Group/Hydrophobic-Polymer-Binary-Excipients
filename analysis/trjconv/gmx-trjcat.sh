gmx trjcat -f ./traj/$title-npt-prod-[0-9]-trunc-[0-9].xtc ./traj/$title-npt-prod-[0-9][0-9]-trunc-[0-9].xtc \
	   -cat -sort \
	   -o ./traj/$title.xtc
