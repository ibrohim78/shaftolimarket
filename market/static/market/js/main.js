const cartCountEl = document.getElementById('cartCount');
const addButtons = Array.from(document.querySelectorAll('.btn-add-cart')).filter(button => button.dataset.name && button.dataset.price);
const cartKey = 'uzumMarketCart';

function getCartCount() {
  const saved = localStorage.getItem(cartKey);
  if (!saved) return 0;
  try {
    const cart = JSON.parse(saved);
    return cart.reduce((sum, item) => sum + item.quantity, 0);
  } catch {
    return 0;
  }
}

function saveCart(cart) {
  localStorage.setItem(cartKey, JSON.stringify(cart));
}

function updateCartCount() {
  if (cartCountEl) {
    cartCountEl.textContent = getCartCount();
  }
}

function addToCart(productName, productPrice) {
  const saved = localStorage.getItem(cartKey);
  const cart = saved ? JSON.parse(saved) : [];
  const existing = cart.find(item => item.name === productName);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ name: productName, price: productPrice, quantity: 1 });
  }
  saveCart(cart);
  updateCartCount();
}

function pulseButton(button) {
  button.classList.add('btn-highlight');
  setTimeout(() => button.classList.remove('btn-highlight'), 300);
}

addButtons.forEach(button => {
  button.addEventListener('click', () => {
    const name = button.dataset.name;
    const price = button.dataset.price;
    addToCart(name, price);
    pulseButton(button);
  });
});

function renderCartPage() {
  const cartTable = document.getElementById('cartTable');
  const cartTotal = document.getElementById('cartTotal');
  const clearButton = document.getElementById('clearCart');
  const emptyMessage = document.getElementById('cartEmpty');

  if (!cartTable || !cartTotal || !clearButton) return;

  const saved = localStorage.getItem(cartKey);
  const cart = saved ? JSON.parse(saved) : [];

  if (cart.length === 0) {
    cartTable.classList.add('hidden');
    emptyMessage.classList.remove('hidden');
    cartTotal.textContent = '0 $';
    return;
  }

  cartTable.classList.remove('hidden');
  emptyMessage.classList.add('hidden');

  const tbody = cartTable.querySelector('tbody');
  tbody.innerHTML = '';

  let total = 0;
  cart.forEach(item => {
    const row = document.createElement('tr');
    const nameCell = document.createElement('td');
    nameCell.textContent = item.name;
    const priceCell = document.createElement('td');
    priceCell.textContent = `$ ${item.price}`;
    const quantityCell = document.createElement('td');
    quantityCell.textContent = item.quantity;
    const subtotalCell = document.createElement('td');
    const subtotal = Number(item.price) * item.quantity;
    subtotalCell.textContent = `$ ${subtotal.toLocaleString()}`;
    row.append(nameCell, priceCell, quantityCell, subtotalCell);
    tbody.appendChild(row);
    total += subtotal;
  });

  cartTotal.textContent = `$ ${total.toLocaleString()}`;

  clearButton.addEventListener('click', () => {
    localStorage.removeItem(cartKey);
    renderCartPage();
    updateCartCount();
  });
}

function renderCheckoutPage() {
  const checkoutTable = document.getElementById('checkoutTable');
  const checkoutTotal = document.getElementById('checkoutTotal');
  const checkoutEmpty = document.getElementById('checkoutEmpty');
  const cartDataInput = document.getElementById('cartData');
  const checkoutForm = document.getElementById('checkoutForm');

  if (!checkoutTable || !checkoutTotal || !cartDataInput || !checkoutForm) return;

  const saved = localStorage.getItem(cartKey);
  const cart = saved ? JSON.parse(saved) : [];

  if (cart.length === 0) {
    checkoutTable.classList.add('hidden');
    checkoutEmpty.classList.remove('hidden');
    checkoutTotal.textContent = '0 $';
    cartDataInput.value = '[]';
    return;
  }

  checkoutTable.classList.remove('hidden');
  checkoutEmpty.classList.add('hidden');

  const tbody = checkoutTable.querySelector('tbody');
  tbody.innerHTML = '';

  let total = 0;
  cart.forEach(item => {
    const row = document.createElement('tr');
    const nameCell = document.createElement('td');
    nameCell.textContent = item.name;
    const priceCell = document.createElement('td');
    priceCell.textContent = `$ ${item.price}`;
    const quantityCell = document.createElement('td');
    quantityCell.textContent = item.quantity;
    const subtotalCell = document.createElement('td');
    const subtotal = Number(item.price) * item.quantity;
    subtotalCell.textContent = `$ ${subtotal.toLocaleString()}`;
    row.append(nameCell, priceCell, quantityCell, subtotalCell);
    tbody.appendChild(row);
    total += subtotal;
  });

  checkoutTotal.textContent = `$ ${total.toLocaleString()}`;
  cartDataInput.value = JSON.stringify(cart);

  checkoutForm.addEventListener('submit', () => {
    if (cart.length === 0) {
      alert('Savatchada mahsulot yo‘q.');
      return false;
    }
  });
}

updateCartCount();
renderCartPage();
renderCheckoutPage();
