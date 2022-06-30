<!DOCTYPE html>
<html dir="ltr" lang="en-US">
<?php include("includes/head.php");?>

<script src="js/jquery.js"></script>
<script src="js/login-uc.js"></script>
<style>
p {margin-bottom: 10px}
</style>
<body class="stretched">
<?php include("includes/body-top.php");?>
<!--<section class="banner">
	  <img src="demos/construction/images/slider/bgsm.png">
	</section>-->

    <section id="content">

        <div class="content-wrap" style="padding-top: 50px;">

            <div class="container clearfix">

                <div class="postcontent nobottommargin clearfix">

                    <div class="row">
                        <div class="col-lg-12">
                            <div class="team team-list clearfix">
                                <div class="team-desc">
                                    <div class="team-title">
                                        <h4>TRUSTID Project - Login UC</h4>
                                    </div>
                                    <div class="team-content">
                                        <div class="row">
                                            <div class="col-md-6 form-group">
                                                <label>Username <small>*</small></label>
                                                <input type="text" id="username" name="username" value="" class="sm-form-control required" />
                                                <br />
                                                <label>Password <small>*</small></label>
                                                <input type="password" id="password" name="password" value="" class="sm-form-control required" />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-6 form-group">
                                                <button id="login-btn" class="button button-border button-rounded">Login</button>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-12 form-group">
                                                <div id="result"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr />

                </div>

                <?php include("includes/sidebar.php");?>

            </div>

        </div>

    </section>
    <!-- #content end -->
<?php include("includes/body-bottom.php");?>
</body>
</html>