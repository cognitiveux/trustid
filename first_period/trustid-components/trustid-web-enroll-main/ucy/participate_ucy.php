<!DOCTYPE html>
<html dir="ltr" lang="en-US">
<?php include("includes/head.php");?>

<script src="js/jquery.js"></script>
<script src="js/subscribe-ucy.js"></script>
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
                    <div class="fancy-title title-bottom-border">
                        <h2>Συμμετοχή σε Έρευνα Χρηστών στα Πλαίσια του Έργου TRUSTID</h2>
                    </div>

                    <div class="row">
                        <div class="col-lg-12">
                            <div class="team team-list clearfix">
                                <div class="team-desc">
                                    <div class="team-title">
                                        <h4>Περιγραφη Ερευνας</h4>
                                    </div>
                                    <div class="team-content">
										<p>Θα θέλαμε να σας προσκαλέσουμε να συμμετάσχετε στην Πρώτη Έρευνα Χρηστών για την αξιολόγηση του TRUSTID. Το TRUSTID είναι ένα Ευρωπαϊκό Έργο που σκοπό έχει να υλοποιήσει και να αξιολογήσει ένα ευφυές σύστημα συνεχούς ταυτοποίησης φοιτητών κατά τη διάρκεια κρίσιμων ακαδημαϊκών δραστηριοτήτων για τη βελτίωση της ασφάλειας και της αξιοπιστίας των συστημάτων ταυτοποίησης στα Ευρωπαϊκά Ιδρύματα Τριτοβάθμιας Εκπαίδευσης. Το TRUSTID αποτελεί μέρος των δράσεων του Erasmus+ 2020 στο πλαίσιο της πρόσκλησης «Στρατηγικές συμπράξεις για την αντιμετώπιση της κατάστασης λόγω της πανδημίας COVID-19 (KA226)».</p>
										<p>Η έρευνα χρηστών θα πραγματοποιηθεί διαδικτυακά μεταξύ <b>24/01/2022 – 28/02/2022 σε τρεις (3) ολιγόλεπτες φάσεις</b> ως εξής:</p>
										<p><b>Φάση 1 (15 λεπτά, τέλη Ιανουαρίου 2021, θα ενημερωθείτε με email και οδηγίες) – Δημιουργία Υπολογιστικών Μοντέλων Ταυτοποίησης</b></p>
										<p>Θα επισκεφθείτε την ιστοσελίδα του έργου η οποία θα σας σταλεί μέσω ηλ. ταχυδρομείου (email) όπου θα ακολουθήσετε απλά βήματα που θα έχουν ως αποτέλεσμα την δημιουργία των υπολογιστικών μοντέλων ταυτοποίησης τα οποία θα βασίζονται στις εικόνες του προσώπου σας.</p>
										<p><b>Φάση 2 (15 λεπτά, αρχές Φεβρουαρίου 2022, θα ενημερωθείτε με email και οδηγίες) – Επαλήθευση και Βελτίωση των Υπολογιστικών Μοντέλων Ταυτοποίησης</b></p>
										<p>Σε αυτή τη φάση θα επισκεφθείτε ξανά την ιστοσελίδα του έργου η οποία θα σας σταλεί και πάλι μέσω ηλ. ταχυδρομείου (email) όπου θα ακολουθήσετε τα ίδια βήματα της Φάσης 1.</p>
										<p><b>Φάση 3 (30 λεπτά, 14/02/2022 – 28/02/2022) – Υλοποίηση της Έρευνας</b></p>
										<p>Θα λάβετε συγκεκριμένες οδηγίες μέσω ηλ. ταχυδρομείου (email) για να συμμετάσχετε στην διαδικτυακή έρευνα.</p>
										<p>Εάν επιθυμείτε  να συμμετάσχετε στην έρευνα, παρακαλούμε δηλώστε συμμετοχή συμπληρώνοντας παρακάτω το ονοματεπώνυμο και την διεύθυνση του ηλ. ταχυδρομείου σας (email).</p>
										<p>Ευχαριστούμε πολύ,</p>
										<p>Η Ομάδα TRUSTID</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr />
                    <div class="row">
                        <div class="col-lg-12">
                            <div class="team team-list clearfix">
                                <div class="team-desc">
                                    <div class="team-title">
                                        <h4>Δηλωση Συμμετοχης εκ μερους του Πανεπιστημιου Κυπρου</h4>
                                    </div>
                                    <div class="team-content">
                                        <div class="row">
                                            <div class="col-md-6 form-group">
                                                <label>Ονοματεπωνυμο <small>*</small></label>
                                                <input type="text" id="name" name="name" value="" class="sm-form-control required" />
                                                <br />
                                                <label>Ηλ. Ταχυδρομειο (Email) <small>*</small></label>
                                                <input type="email" id="email" name="email" value="" class="sm-form-control required" />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-6 form-group">
                                                <button id="subscribe" class="button button-border button-rounded">Δηλωση Συμμετοχης</button>
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
                    <div class="row">
                        <div class="col-lg-12">
                            <div class="team team-list clearfix">
                                <div class="team-desc">
                                    <div class="team-title">
                                        <h4>Ερευνητικη Δεοντολογια και Ιδιωτικοτητα Προσωπικων Δεδομενων</h4>
                                    </div>
                                    <div class="team-content">
                                        <p>Η έρευνα χρηστών και η επεξεργασία των δεδομένων θα αντιμετωπίζονται με βάση σύγχρονων προτύπων όσον αφορά την ερευνητική δεοντολογία
                                            και την προστασία της ιδιωτικότητας προσωπικών δεδομένων. Συγκεκριμένα, η έρευνα συμμορφώνεται με τους κανονισμούς
                                            και τις κατευθυντήριες γραμμές για την ερευνητική δεοντολογία και την προστασία της ιδιωτικότητας προσωπικών δεδομένων,
                                            όπως ο κώδικας επαγγελματικής συμπεριφοράς του User Experience Professionals Association (UXPA -
                                            <a href="https://uxpa.org/uxpa-code-of-professional-conduct" target="_blank">https://uxpa.org/uxpa-code-of-professional-conduct</a>).
                                            Η έρευνα συμμορφώνεται επίσης με τον σχετικό κανονισμό, τις αρχές και τη νομοθεσία της Ευρωπαϊκής Επιτροπής και ιδιαίτερα με εκείνες
                                            που αφορούν τη συμμετοχή ενηλίκων σε μελέτες χρηστών (<a href="https://ec.europa.eu/programmes/horizon2020/en/h2020-section/ethics" target="_blank">https://ec.europa.eu/programmes/horizon2020/en/h2020-section/ethics</a>).
                                            Οι συμμετέχοντες θα ενημερωθούν και θα απαιτηθεί η συγκατάθεσή τους για τη συμμετοχή τους. 
											Τα δεδομένα θα είναι εμπιστευτικά και θα επεξεργάζονται και θα αποθηκεύονται με ασφάλεια καθ' όλη τη διάρκεια του έργου.
											Στο τέλος του έργου, όλα τα δεδομένα θα διαγραφούν οριστικά από τη βάση δεδομένων του έργου. 
											Πρόσβαση στα δεδομένα θα έχουν μόνο ερευνητές του έργου και θα χρησιμοποιηθούν μόνο για ερευνητικούς σκοπούς. 
										</p>
											<p>
											<b>Αποχώρηση από τη Μελέτη και Διαγραφή των Δεδομένων σας</b><br />
											Οι συμμετέχοντες μπορούν να αποφασίσουν να αποχωρήσουν από την έρευνα ανά πάσα στιγμή. 
											Στην περίπτωση όπου συμμετέχοντας χρήστης επιθυμεί να αποχωρήσει από την έρευνα, όλα τα 
											δεδομένα του συμμετέχοντα χρήστη θα σβήνονται ολοκληρωτικά από τα αρχεία της ερευνητικής ομάδας. 
											Σε περίπτωση που επιθυμείτε να διαγραφούν τα δεδομένα σας, παρακαλούμε όπως αποστείλετε ένα μήνυμα στο 
											<a href="mailto:unscubscribe_poc1@trustid-project.eu">unscubscribe_poc1@trustid-project.eu</a> χρησιμοποιώντας το ίδιο email που χρησιμοποιήσατε κατά την 
											εγγραφή σας στη μελέτη χρηστών και τότε όλα τα δεδομένα σας θα διαγραφούν οριστικά από τη βάση δεδομένων του έργου.
											</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

                <?php include("includes/sidebar.php");?>

            </div>

        </div>

    </section>
    <!-- #content end -->
<?php include("includes/body-bottom.php");?>
</body>
</html>