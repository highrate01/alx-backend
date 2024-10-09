import express from 'express';
import redis from 'redis';

const client = redis.createClient();

client.on('error', (err) => console.log('Redis Client Error', err));

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

function getItemById (id) {
  return listProducts.find(product => product.itemId === id);
}

async function reserveStockById (itemId, stock) {
  return new Promise((resolve, reject) => {
    client.set(`item.${itemId}`, stock, (err, reply) => {
      if (err) reject(err);
      resolve(reply);
    });
  });
}

async function getCurrentReservedStockById (itemId) {
  return new Promise((resolve, reject) => {
    client.get(`item.${itemId}`, (err, reply) => {
      if (err) reject(err);
      resolve(reply);
    });
  });
}

const app = express();
const port = 1245;

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  if (isNaN(itemId)) {
    return res.status(400).json({ status: 'Invalid item ID' });
  }
  const product = getItemById(itemId);
  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }
  try {
    const currentStock = await getCurrentReservedStockById(itemId) || product.initialAvailableQuantity;
    res.json({
      ...product,
      currentQuantity: Number(currentStock)
    });
  } catch (err) {
    res.status(500).json({ status: 'Server error', message: err.message });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  if (isNaN(itemId)) {
    return res.status(400).json({ status: 'Invalid item ID' });
  }
  const product = getItemById(itemId);
  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }
  try {
    const currentStock = Number(await getCurrentReservedStockById(itemId) || product.initialAvailableQuantity);
    if (currentStock <= 0) {
      return res.status(400).json({ status: 'Not enough stock available', itemId });
    }
    const newStock = currentStock - 1;
    await reserveStockById(itemId, newStock);
    res.json({ status: 'Reservation confirmed', itemId });
  } catch (err) {
    res.status(500).json({ status: 'Server error', message: err.message });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
