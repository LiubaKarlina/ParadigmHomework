module Tree (BinaryTree, insert, lookup, delete) where
import Prelude hiding (lookup)

-- Реализовать двоичное дерево поиска без балансировки (4 балла)
data BinaryTree k v = Empty | Node k v (BinaryTree k v) (BinaryTree k v) deriving (Show, Eq, Ord)

key :: BinaryTree k v -> k
key (Node k v l r) = k

value :: BinaryTree k v -> v
value (Node k v l r) = v

-- “Ord k =>” требует, чтобы элементы типа k можно было сравнивать 
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k Empty = Nothing 
lookup k (Node tk tv left right)
                   | k == tk = Just tv
                   | k < tk  = lookup k left
                   | otherwise  = lookup k right


insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Empty = Node k v Empty Empty 
insert k v (Node tk tv left right)
                   | k == tk = (Node k v left right)
                   | k < tk  = (Node tk tv (insert k v left) right)
                   | otherwise  = (Node tk tv left (insert k v right))

siftUp :: BinaryTree k v -> BinaryTree k v
siftUp Empty = Empty
siftUp (Node k v Empty Empty) = Empty
siftUp (Node k v Empty right) = (Node (key right) (value right) Empty        (siftUp right))
siftUp (Node k v left  right) = (Node (key left)  (value left)  (siftUp left) right        )  

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Empty = Empty
delete k (Node tk tv left right)
                   | k < tk = (Node tk tv (delete k left) right)
                   | k > tk = (Node tk tv left (delete k right))
                   | otherwise = siftUp (Node tk tv left right) 

