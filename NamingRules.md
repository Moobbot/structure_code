# Quy Tắc viết trong dự án

## Table of Contents

- [Quy Tắc viết trong dự án](#quy-tắc-viết-trong-dự-án)
  - [Table of Contents](#table-of-contents)
  - [1. Quy định chung](#1-quy-định-chung)
    - [1.1. Đặt tên Biến, Hàm, và Class:](#11-đặt-tên-biến-hàm-và-class)
    - [1.2. Viết mô tả (Docstrings):](#12-viết-mô-tả-docstrings)
  - [2. Quy tắc viết Code OOP](#2-quy-tắc-viết-code-oop)
    - [2.1. `Encapsulation (Đóng Gói)`:](#21-encapsulation-đóng-gói)
    - [2.2. `Inheritance (Kế Thừa)`:](#22-inheritance-kế-thừa)
    - [2.3. `Polymorphism (Đa Hình)`:](#23-polymorphism-đa-hình)
    - [2.4. `Abstraction (Trừu Tượng)`:](#24-abstraction-trừu-tượng)
  - [3. Quy Tắc Viết Code Khác](#3-quy-tắc-viết-code-khác)
  - [4. Quản Lý Dependencies và Environment](#4-quản-lý-dependencies-và-environment)
    - [Sử Dụng `Virtual Environment`:](#sử-dụng-virtual-environment)
    - [Quản Lý `Dependencies` Bằng `requirements.txt`:](#quản-lý-dependencies-bằng-requirementstxt)
    - [Sử Dụng `setup.py` cho các dự án lớn:](#sử-dụng-setuppy-cho-các-dự-án-lớn)

## 1. Quy định chung

### 1.1. Đặt tên Biến, Hàm, và Class:

- Biến: `snake_case` (vd: `` my_variable`)
- Hàm: `snake_case` (vd:  ``my_function`)
- Class: `PascalCase`(vd:`MyClass`)
- Hằng Số: `UPPER_SNAKE_CASE`(vd:`MY_CONSTANT`)

### 1.2. Viết mô tả (Docstrings):

- Sử dụng docstring để mô tả các class, method, và function.
- Docstring nên bao gồm mô tả chức năng, các tham số, và giá trị trả về.

```py
class MyClass:
    """
    Mô tả class MyClass.

    Attributes:
        attr1 (type): Mô tả attr1.
        attr2 (type): Mô tả attr2.
    """

    def __init__(self, attr1, attr2):
        """
        Khởi tạo MyClass.

        Args:
            attr1 (type): Mô tả attr1.
            attr2 (type): Mô tả attr2.
        """
        self.attr1 = attr1
        self.attr2 = attr2

    def my_method(self, param1):
        """
        Mô tả method.

        Args:
            param1 (type): Mô tả param1.

        Returns:
            type: Mô tả giá trị trả về.
        """
        pass
```

## 2. Quy tắc viết Code OOP

### 2.1. `Encapsulation (Đóng Gói)`:

- Sử dụng biến private (`__`) và protected (`_`) để kiểm soát truy cập.

```py
class MyClass:
    def __init__(self, public_attr, protected_attr, private_attr):
        self.public_attr = public_attr
        self._protected_attr = protected_attr
        self.__private_attr = private_attr
```

### 2.2. `Inheritance (Kế Thừa)`:

- Sử dụng kế thừa để chia sẻ chức năng giữa các class có liên quan.

```py
class BaseClass:
    def __init__(self, base_attr):
        self.base_attr = base_attr

    def base_method(self):
        pass
```

```py
class DerivedClass(BaseClass):
    def __init__(self, base_attr, derived_attr):
        super().__init__(base_attr)
        self.derived_attr = derived_attr

    def derived_method(self):
        pass
```

### 2.3. `Polymorphism (Đa Hình)`:

- Sử dụng đa hình để xử lý các đối tượng khác nhau thông qua cùng một interface.

```py
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"
```

### 2.4. `Abstraction (Trừu Tượng)`:

- Sử dụng abstract class và method để định nghĩa các phương thức trừu tượng cần được implement trong các lớp con.

```py
from abc import ABC, abstractmethod

class AbstractClass(ABC):
    @abstractmethod
    def abstract_method(self):
        pass
```

```py
class ConcreteClass(AbstractClass):
    def abstract_method(self):
        pass
```

## 3. Quy Tắc Viết Code Khác

- Tuân Thủ `PEP 8`:

  - Sử dụng chuẩn [PEP 8 Style Guide](https://peps.python.org/pep-0008/) cho coding style

- Sử dụng `Black Formatter`

  - Sử dụng [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) cho coding style

- Sử dụng `Type Hints`:

  - Sử dụng `type hints` để tăng cường tính rõ ràng và giúp kiểm tra lỗi.

```py
def my_function(param1: int, param2: str) -> bool:
    return True
```

- Viết `Test Unit`:
  - Mỗi class và method nên có unit test để kiểm tra tính đúng đắn.

```py
import unittest

class TestMyClass(unittest.TestCase):
    def test_my_method(self):
        obj = MyClass(1, 2)
        self.assertEqual(obj.my_method(), expected_value)
```

- Sử dụng `Logging` thay cho `Print`:
  - Sử dụng module logging để ghi log thay vì dùng print.

```py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Thông tin log")
```

- Sử dụng `Context Manager`:
  - Sử dụng `with` statement để quản lý tài nguyên như file, kết nối database.

```py
with open('file.txt', 'r') as file:
    content = file.read()
```

## 4. Quản Lý Dependencies và Environment

### Sử Dụng `Virtual Environment`:

- Sử dụng `virtual environment` để quản lý `dependencies` cho mỗi dự án.

```sh
python -m venv env
source env/bin/activate
```

### Quản Lý `Dependencies` Bằng `requirements.txt`:

- Liệt kê tất cả các `dependencies` trong file `requirements.txt`.

```sh
pip freeze > requirements.txt
```

### Sử Dụng [`setup.py`](https://pythonhosted.org/an_example_pypi_project/setuptools.html) cho các dự án lớn:

- Sử dụng [`setup.py`](setup.example.py) để tạo và quản lý các package.
