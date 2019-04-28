require_once("config.inc");
require_once("util.inc");
require_once("service-utils.inc");

function usage() {
	echo "Usage: playback provision <gateway> <wan> <lan> <opt1>";
	echo "Examples:\n";
	echo "playback provision 192.168.0.1 192.168.0.2/24 10.0.1.1/24 10.0.2.1/24\n";
	echo "\n";
}

global $g, $config, $argv, $command_split;

if (is_array($command_split)) {
	$args = array_slice($command_split, 2);
} else {
	$args = array_slice($argv, 3);
}

if (empty($args[0]) || count($args) != 4) {
	usage();
}

# Reload config
parse_config(true);

# Configuration
$gateway = $args[0];
$interfaces = array(
	'wan'  => explode('/', $args[1]),
	'lan'  => explode('/', $args[2]),
	'opt1' => explode('/', $args[3])
);

# Configure Interfaces
foreach ( $interfaces AS $if => $cfg ) {
	$config['interfaces'][$if]['ipaddr'] = $cfg[0];
	$config['interfaces'][$if]['subnet'] = $cfg[1];
}

# Configure Gateway
$config['gateways']['gateway_item'][0]['gateway'] = $gateway;

# Save config
write_config();

# Cleanup logs
! rm -rf /var/log/*
! rm /etc/ssh/ssh_host_*_key*

# Reboot
system_reboot_sync();