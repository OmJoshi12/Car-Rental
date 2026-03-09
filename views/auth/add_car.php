<?php
require_once '../config/config.php';
require_once '../controllers/CarController.php';

$auth = new AuthController();
$auth->requireAgency();

$carController = new CarController();
$error = '';
$success = '';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $vehicle_model = trim($_POST['vehicle_model'] ?? '');
    $vehicle_number = trim($_POST['vehicle_number'] ?? '');
    $seating_capacity = $_POST['seating_capacity'] ?? '';
    $rent_per_day = $_POST['rent_per_day'] ?? '';
    
    $result = $carController->addCar($vehicle_model, $vehicle_number, $seating_capacity, $rent_per_day);
    
    if ($result['success']) {
        $_SESSION['success'] = $result['message'];
        header('Location: agency_dashboard.php');
        exit();
    } else {
        $error = $result['message'];
    }
}

$page_title = 'Add New Car - Premium Car Rental';
ob_start();
?>

<!-- Hero Section -->
<section class="hero" style="padding: 3rem 0;">
    <div class="container">
        <h1>Add New Car</h1>
        <p>Add a new vehicle to your rental fleet</p>
    </div>
</section>

<!-- Add Car Form -->
<section class="mb-4">
    <div class="container">
        <div class="row">
            <div class="col-md-8" style="margin: 0 auto;">
                <div class="card">
                    <div class="card-header">
                        <h3>Car Details</h3>
                    </div>
                    <div class="card-body">
                        <?php if ($error): ?>
                            <div class="alert alert-error">
                                <?= htmlspecialchars($error) ?>
                            </div>
                        <?php endif; ?>

                        <form method="POST" data-validate>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="vehicle_model" class="form-label">Vehicle Model *</label>
                                        <input type="text" id="vehicle_model" name="vehicle_model" class="form-control" 
                                               value="<?= htmlspecialchars($_POST['vehicle_model'] ?? '') ?>" 
                                               required placeholder="e.g., Toyota Camry">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="vehicle_number" class="form-label">Vehicle Number *</label>
                                        <input type="text" id="vehicle_number" name="vehicle_number" class="form-control" 
                                               value="<?= htmlspecialchars($_POST['vehicle_number'] ?? '') ?>" 
                                               required placeholder="e.g., ABC-1234"
                                               pattern="[A-Za-z]{2,3}-[0-9]{4}"
                                               title="Format: ABC-1234">
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="seating_capacity" class="form-label">Seating Capacity *</label>
                                        <select id="seating_capacity" name="seating_capacity" class="form-select" required>
                                            <option value="">Select Seating Capacity</option>
                                            <?php for ($i = 1; $i <= 10; $i++): ?>
                                                <option value="<?= $i ?>" <?= ($_POST['seating_capacity'] ?? '') == $i ? 'selected' : '' ?>><?= $i ?> Seats</option>
                                            <?php endfor; ?>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label for="rent_per_day" class="form-label">Rent Per Day (USD) *</label>
                                        <input type="number" id="rent_per_day" name="rent_per_day" class="form-control" 
                                               value="<?= htmlspecialchars($_POST['rent_per_day'] ?? '') ?>" 
                                               required placeholder="e.g., 50.00" min="0.01" step="0.01">
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">
                                    Add Car
                                </button>
                            </div>
                        </form>

                        <div class="text-center mt-3">
                            <a href="agency_dashboard.php" class="btn btn-outline">Back to Dashboard</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<?php
$content = ob_get_clean();
require_once '../views/layouts/main.php';
?>
