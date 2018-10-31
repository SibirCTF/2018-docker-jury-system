#!/usr/bin/perl

use strict;
use warnings FATAL => 'all';
use IO::Socket;
use JSON;
use Digest::MD5 qw(md5_hex);
use IO::Socket::Timeout;
use Try::Tiny;
use File::Spec;
use File::Basename;

my $dir = dirname(File::Spec->rel2abs(__FILE__));

my $port = "8080";

my %hash = (
	"service is worked" => 101,
	"service is corrupt" => 102,
	"service is mumble" => 103,
	"service is down" => 104,
);

sub list_task{
	my $random_ntask = int(rand(100));
	return $random_ntask;
}

sub open_task {
	my $task = shift;
	my $h = "";
	open FILE, "$dir/json/taskseng";
	while (my $line = <FILE>) {
		$h = $h.$line;
	} 
	close FILE;
	my @b = split(/\n\n/, $h);
	return @b;
}

sub open_code {
	my $task = shift;
	my $h = "";
	open FILE, "$dir/json/tasks/$task.c";
	while (my $line = <FILE>) {
		$h = $h.$line;
	} 
	close FILE;
	return $h;
}

sub create_json {
	my ($ntask, $id_flag, $ip_addr) = @_;
	my @task_list = open_task();
	my @task = split(/\n/, $task_list[$ntask]);
	my $json = {
		"description" => $task[0],
		"input" => $task[1],
		"output" => $task[2],
		"code_n" => $ntask,
		"ndb_task" => "",
	};
	my $json2 = JSON->new->utf8->encode($json);
	if (-e "$dir/json/$ip_addr") { 
		open FILE, ">> $dir/json/$ip_addr/$id_flag.json";	
		print FILE $json2;
		close FILE;
	} else {
		mkdir "$dir/json/$ip_addr", 4555;
		open FILE, ">> $dir/json/$ip_addr/$id_flag.json";	
		print FILE $json2;
		close FILE;
	}
}

sub open_json {
	my ($flag_id, $ip_addr) = @_;
	my $h = "";
	open FILE, "$dir/json/$ip_addr/$flag_id.json";
	while (my $line = <FILE>) {
		$h = $h.$line;
	} 
	close FILE;
	my $json = decode_json($h);
	return $json;
}

sub fix_json {
	my ($flag_id, $ndb_task, $ip_addr) = @_;
	my $a = "";
	open FILE, "$dir/json/$ip_addr/$flag_id.json";
	while (my $line = <FILE>){
		$a = $a.$line;
	}	
	close FILE;
	my $json = decode_json($a);
	$json->{"ndb_task"} = $ndb_task;
	my $json2 = JSON->new->utf8->encode($json);
	open FILE, "> $dir/json/$ip_addr/$flag_id.json";
	print FILE $json2;	
	close FILE;
}


sub registration {
	my ($socket, $login, $pass, $role) = @_;
	my $answer = <$socket>;
	print $socket "$login\n";
	$answer = <$socket>;
	print $socket "$pass\n";
	$answer = <$socket>;
	if ($role eq "w") {
		print $socket "w\n"; #| or r
	} else {
		print $socket "r\n"; #| or r
	}
}

sub log_in {
	my ($socket, $login, $pass) = @_;
	my $answer = <$socket>;
	print $socket "$login\n";
	$answer = <$socket>;
	print $socket "$pass\n";
}

sub put_flag {
	my ($ip_addr, $id_flag, $flag) = @_;
	my $socket = IO::Socket::INET->new(
		PeerAddr => $ip_addr,
	        PeerPort => $port,
	        Proto => "tcp",
		Type => SOCK_STREAM,
	) or return $hash{"service is down"};
	IO::Socket::Timeout->enable_timeouts_on($socket);
	$socket->read_timeout(3);	
	$socket->write_timeout(3);
	
	registration($socket, "w$id_flag", md5_hex("w$id_flag"), "w");
	my $answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	print $socket "1\n";
	$answer = <$socket>;
	my $res = open_json($id_flag, $ip_addr);
	my $description = $res->{"description"};
	print $socket "$description\n\n";
	$answer = <$socket>;
	print $socket "$flag\n"; 
	$answer = <$socket>;
	my $ndb_task;
	if ($answer =~ m/\d+/) {
		$ndb_task = $&;
	} else {
		close($socket);
		return $answer;
	}
	$answer = <$socket>;
	close($socket);
	fix_json($id_flag, $ndb_task, $ip_addr);
	return $answer;
}

sub put_test {
	my ($ip_addr, $id_flag, $flag) = @_;	
	my $socket = IO::Socket::INET->new(
		PeerAddr => $ip_addr,
	        PeerPort => $port,
	        Proto => "tcp",
		Type => SOCK_STREAM,
	) or return $hash{"service is down"};

	IO::Socket::Timeout->enable_timeouts_on($socket);
	$socket->read_timeout(3);	
	$socket->write_timeout(3);

	log_in($socket, "w$id_flag", md5_hex("w$id_flag"));
	my $answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	print $socket "2\n";
	$answer = <$socket>;
	my $res = open_json($id_flag, $ip_addr);
	my $ndb_task = $res->{"ndb_task"};
	print $socket "$ndb_task\n"; 
	$answer = <$socket>;
	my $input = $res->{"input"};
	print $socket "$input\n";
	$answer = <$socket>;
	my $output = $res->{"output"};
	print $socket "$output\n";
	$answer = <$socket>;
	$answer = <$socket>;
	close($socket);
	return $answer;
}

sub get_task{
	my ($ip_addr, $id_flag, $flag) = @_;
	my $socket = IO::Socket::INET->new(
		PeerAddr => $ip_addr,
	        PeerPort => $port,
	        Proto => "tcp",
		Type => SOCK_STREAM,
	) or return $hash{"service is down"};
	
	IO::Socket::Timeout->enable_timeouts_on($socket);
	$socket->read_timeout(3);	
	$socket->write_timeout(3);
	
	registration($socket, "r$id_flag", md5_hex("r$id_flag"), "r");
	my $answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	print $socket "1\n";
	$answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	my $res = open_json($id_flag, $ip_addr);
	my $ndb_task = $res->{"ndb_task"};
	print $socket "$ndb_task\n";
	$answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	close($socket);
	return $answer;	
}

sub pass_task {
	my ($ip_addr, $id_flag, $flag) = @_;
	my $socket = IO::Socket::INET->new(
		PeerAddr => $ip_addr,
	        PeerPort => $port,
	        Proto => "tcp",
		Type => SOCK_STREAM, 
	) or return $hash{"service is down"};

	IO::Socket::Timeout->enable_timeouts_on($socket);
	$socket->read_timeout(3);	
	$socket->write_timeout(3);

	log_in($socket, "r$id_flag", md5_hex("r$id_flag"));
	my $answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	print $socket "2\n";
	$answer = <$socket>;
	my $res = open_json($id_flag, $ip_addr);
	my $ndb_task = $res->{"ndb_task"};
	print $socket "$ndb_task\n";
	$answer = <$socket>;
	my $task = open_code($res->{"code_n"});
	print $socket "$task\n\n"; 
	$answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	close $socket;
	return $answer;
}

sub check_task {
	my ($ip_addr, $id_flag, $flag) = @_;
	my $socket = IO::Socket::INET->new(
		PeerAddr => $ip_addr,
	        PeerPort => $port,
	        Proto => "tcp",
		Type => SOCK_STREAM,
	) or return $hash{"service is down"};

	IO::Socket::Timeout->enable_timeouts_on($socket);
	$socket->read_timeout(3);	
	$socket->write_timeout(3);

	log_in($socket, "w$id_flag", md5_hex("w$id_flag"));
	my $answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	$answer = <$socket>;
	print $socket "3\n";
	$answer = <$socket>;
	my $res = open_json($id_flag, $ip_addr);
	my $ndb_task = $res->{"ndb_task"};
	print $socket "$ndb_task\n";
	$answer = <$socket>;
	my $flag2 = "";
	if ($answer =~ m/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}/) {
		$flag2 = $&;
	} else {
		return $hash{"service is corrupt"};
	}
	$answer = <$socket>;
	close $socket;
	if ($answer ne "Press ctrl+c for exit\n") {
		return $hash{"service is corrupt"};
	}
	if ($flag eq $flag2) {
		return $hash{"service is worked"};
	} else {
		return $hash{"service is corrupt"};
	}	
}

sub checker {	
	my $ip_addr = $ARGV[0];	
	my $id_flag = "$ARGV[2]";
	my $flag = $ARGV[3];
	my $command = $ARGV[1];

	if ($command eq "put") {
		my $task = list_task();
		create_json($task, $id_flag, $ip_addr);	
		try {
			my $res = put_flag($ip_addr, $id_flag, $flag);
			if ($res =~ /^\d+$/) {
				return $hash{"service is down"};
			} 
			if ($res ne "Press ctrl+c for exit\n") {
				return $hash{"service is corrupt"};
			}
			$res = put_test($ip_addr, $id_flag, $flag);
			if ($res =~ /^\d+$/) {
				return $hash{"service is down"};
			} 
			if ($res ne "Press ctrl+c for exit\n") {
				return $hash{"service is corrupt"};
			} 
			$res = get_task($ip_addr, $id_flag, $flag);
			if ($res =~ /^\d+$/) {
				return $hash{"service is down"};
			} 
			if ($res ne "Press ctrl+c for exit\n") {
				return $hash{"service is corrupt"};
			}
			$res = pass_task($ip_addr, $id_flag, $flag);
			if ($res =~ /^\d+$/) {
				return $hash{"service is down"};
			} 
			if ($res ne "Press ctrl+c for exit\n") {
				return $hash{"service is corrupt"};
			}
			return $hash{"service is worked"};
		}
		catch {
			return $hash{"service is mumble"};
		}
	} elsif ($command eq "check") {
		try {
			return check_task($ip_addr, $id_flag, $flag);
		}
		catch {
			return $hash{"service is mumble"};
		}
	}
}

my $code = checker();
if ($code == 101) {
	print "[service is worked] - 101";
}
if ($code == 102) {
	print "[service is corrupt] - 102";
}
if ($code == 103) {
	print "[service is mumble] - 103";
}
if ($code == 104) {
	print "[service is down] - 104";
}
exit $code;
