
#connect to the db before we waste time loading the spells file
my $source1 = "DBI:mysql:database=information_schema;host=$host";
my $source2 = "DBI:mysql:database=$db;host=$host";

#pull the column names from the db so we don't have to maintain a list. should also help if there are more columns in the db than the spells file
my $dbh = DBI->connect($source1, $user, $pass) || die "Could not create db handle\n";
my $sth = $dbh->prepare("SELECT COLUMN_NAME FROM COLUMNS WHERE TABLE_SCHEMA='$db' AND TABLE_NAME='$table' ORDER BY ORDINAL_POSITION ASC");
$sth->execute(); #run the query on the db
#create an array of the column names. i have a feeling there might be a more direct way to do it, but oh well
while (my $val = $sth->fetch()) {
	push(@col_names, @$val[0]); # $column[#]
}

#switch to the emu db
$dbh = DBI->connect($source2, $user, $pass) || die "Could not create db handle\n";

if ($opt_d) { #drop all data in the spells table
	print "Are you sure you want to erase all spells from the '$table' table?\n";
	print "y/N ? ";
	my $confirm = <STDIN>;
	if ($confirm=~/^y/i) { #as long as it begins with a Y, that's the important part
		print "Deleting spells from the '$table' table... ";
		$dbh->do("DELETE from $table");
		print "Done.\n\n";
	} else {
		print "\nSkipping erasing spells from the '$table' table\n\n";
	}
}

#open spell file
open(SPELLS, "<$spellf") or die "Unable to open spells: $spellf\n";
#parse through spells
my($numspells, $loadedspells, $highid); #define some variables, cause we're cool like that
while(<SPELLS>) {
	++$numspells;

	chomp(); #get rid of those pesky new lines
	s/'/\\'/g; #make query safe(r) by escaping quotes (\')
	@s = split(/\^/); #separate by the ^ delimiter

	my @t_col_names = @col_names; #so we can safely pop any unneeded columns, but still have all of them the next time around
	my $col_diff = abs(scalar(@t_col_names) - scalar(@s)); #we need to find out if the db or spells file has more columns, so we don't blow something up. this will get the amount of extra columns
	#we're going to do this each loop, just in case someone screws up a line in the spell file, or starts messing with the table in the middle of the import
	if (scalar(@s) < scalar(@t_col_names)) {
		for (my $z = 1; $z <= $col_diff; $z++) {
			pop(@t_col_names);
		}
	} elsif (scalar(@s) > scalar(@t_col_names)) {
		for (my $z = 1; $z <= $col_diff; $z++) {
			pop(@s);
		}
	}

	my $insert1 = join("`,`", @t_col_names);
	my $insert2 = join("','", @s); #put everything in quotes & separate w/ commas for the query, plus the beginning & ending quotes. this doesn't print out to the console correctly (for me), but hopefully the query will be fine
	my $insert = sprintf("REPLACE INTO %s (`%s`) VALUES ('%s')", $table, $insert1, $insert2);

	printf("Loading \"%s\" (%d)                     \r", $s[1], $s[0]); # name (id)

	my $i = $dbh->do($insert); #put these bad boys into the db
	if ($i < 1) { #if the query didn't update anything into the db, or errored
		printf("Error loading \"%s\" (%s)                     \n", $s[1], $s[0]);
	} else {
		$loadedspells++; #to compare db inserts to total spells
	}

	$highid = $s[0]; #set to current id
}

print "Spells Loaded: $loadedspells of $numspells                     \n";
print "Highest ID: $highid\n\n";