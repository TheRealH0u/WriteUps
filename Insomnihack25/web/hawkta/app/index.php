<?php

// Authorized images are matched to their bcrypt hash values for maximum security
$AUTHORIZED_IMGS = [
    '$2a$12$NmPFGriPq4VEFdx7y4XKde67/DFQgQVk/Cz.HxGWi0PV3aSk/JT12' => 'assets/data/img/cooper-s-hawk-profile-583855629-d89e191a88d1484db08800f067ba98e8.jpg',
    '$2a$12$qsfcrstGdzpRVDNH5Dq//uSK6/Z6ZSBCca7fIeoyRBBdgQk8q3rX6' => 'assets/data/img/Red-shouldered_Hawk_Buteo_lineatus_-_Blue_Cypress_Lake_Florida.jpg',
    '$2a$12$hPNstQ8F.EBu8z2/EDaXROPakN5L/hix0SUQQG6I6RPu/BcvSBDmC' => 'assets/data/img/harris_hawk_web.jpg',
    '$2a$12$dp0lDL1FuN6irg2LB7j.EOFKte1313GSgz5DpBeTAtBY4gyCMd4KS' => 'assets/data/img/Hawk-146809760-612x612.jpg',
    '$2a$12$5zq3d97d5wg1vUvoquZOA.JAeM1.778eWnDgSx/ymj9v1D8d4kLEC' => 'assets/data/img/Hawk-534214314-612x612.jpg', 
    //'$2a$12$v5UW4B3/j6F5vymG0tRDx.iSz7RFlrVlH3Om3zC3QfqiG.InCuKMW' => 'flag.txt'
];

if (empty($_GET)) {
    include 'index.html';
    exit();
}

$file_name = isset($_GET['file']) ? (string) $_GET['file'] : null;
$provided_hash = isset($_GET['hash']) ? (string) $_GET['hash'] : null;

if (!$file_name || !$provided_hash) {
    http_response_code(400);
    exit("Missing 'file' or 'hash' parameter.");
}

// Check if the file is authorized and the hash is valid
if (isset($AUTHORIZED_IMGS[$provided_hash]) && password_verify($file_name, $provided_hash)) {

        header("Content-Type: image/png");
        echo readfile($file_name);
        exit();
}

// If no match, return forbidden
http_response_code(403);
exit("Invalid file or hash.");

?>
