use std::fmt;
use std::hash::{Hash, Hasher};
use std::ops::Deref;

#[derive(Copy, Clone)]
pub struct Float32 {
    value: f32,
}
impl Float32 {
    pub fn new(value: f32) -> Float32 {
        return Float32 { value: value };
    }
}
impl Hash for Float32 {
    fn hash<H: Hasher>(&self, state: &mut H) {
        unsafe {
            std::mem::transmute::<f32, u32>(self.value).hash(state);
        }
    }
}
impl PartialEq<Float32> for Float32 {
    fn eq(&self, other: &Float32) -> bool {
        self.value == other.value
    }
}
impl PartialEq<f32> for Float32 {
    fn eq(&self, other: &f32) -> bool {
        &self.value == other
    }
}
impl Eq for Float32 {}
impl std::ops::Add<Float32> for Float32 {
    type Output = Float32;

    fn add(self, _rhs: Float32) -> Float32 {
        Float32::new(self.value + _rhs.value)
    }
}
impl std::ops::AddAssign<Float32> for Float32 {
    fn add_assign(&mut self, _rhs: Float32) {
        self.value += _rhs.value
    }
}
impl std::ops::Add<f32> for Float32 {
    type Output = Float32;

    fn add(self, _rhs: f32) -> Float32 {
        Float32::new(self.value + _rhs)
    }
}
impl std::ops::AddAssign<f32> for Float32 {
    fn add_assign(&mut self, _rhs: f32) {
        self.value += _rhs
    }
}
impl std::ops::Sub<Float32> for Float32 {
    type Output = Float32;

    fn sub(self, _rhs: Float32) -> Float32 {
        Float32::new(self.value - _rhs.value)
    }
}
impl std::ops::SubAssign<Float32> for Float32 {
    fn sub_assign(&mut self, _rhs: Float32) {
        self.value -= _rhs.value
    }
}
impl std::ops::Sub<f32> for Float32 {
    type Output = Float32;

    fn sub(self, _rhs: f32) -> Float32 {
        Float32::new(self.value - _rhs)
    }
}
impl std::ops::SubAssign<f32> for Float32 {
    fn sub_assign(&mut self, _rhs: f32) {
        self.value -= _rhs
    }
}
impl std::ops::Mul<Float32> for Float32 {
    type Output = Float32;

    fn mul(self, _rhs: Float32) -> Float32 {
        Float32::new(self.value * _rhs.value)
    }
}
impl std::ops::MulAssign<Float32> for Float32 {
    fn mul_assign(&mut self, _rhs: Float32) {
        self.value *= _rhs.value
    }
}
impl std::ops::Mul<f32> for Float32 {
    type Output = Float32;

    fn mul(self, _rhs: f32) -> Float32 {
        Float32::new(self.value * _rhs)
    }
}
impl std::ops::MulAssign<f32> for Float32 {
    fn mul_assign(&mut self, _rhs: f32) {
        self.value *= _rhs
    }
}
impl std::ops::Div<Float32> for Float32 {
    type Output = Float32;

    fn div(self, _rhs: Float32) -> Float32 {
        Float32::new(self.value / _rhs.value)
    }
}
impl std::ops::DivAssign<Float32> for Float32 {
    fn div_assign(&mut self, _rhs: Float32) {
        self.value /= _rhs.value
    }
}
impl std::ops::Div<f32> for Float32 {
    type Output = Float32;

    fn div(self, _rhs: f32) -> Float32 {
        Float32::new(self.value / _rhs)
    }
}
impl std::ops::DivAssign<f32> for Float32 {
    fn div_assign(&mut self, _rhs: f32) {
        self.value /= _rhs
    }
}
impl std::ops::Rem<Float32> for Float32 {
    type Output = Float32;

    fn rem(self, _rhs: Float32) -> Float32 {
        Float32::new(self.value % _rhs.value)
    }
}
impl std::ops::RemAssign<Float32> for Float32 {
    fn rem_assign(&mut self, _rhs: Float32) {
        self.value %= _rhs.value
    }
}
impl std::ops::Rem<f32> for Float32 {
    type Output = Float32;

    fn rem(self, _rhs: f32) -> Float32 {
        Float32::new(self.value % _rhs)
    }
}
impl std::ops::RemAssign<f32> for Float32 {
    fn rem_assign(&mut self, _rhs: f32) {
        self.value %= _rhs
    }
}
impl std::ops::Neg for Float32 {
    type Output = Float32;

    fn neg(self) -> Float32 {
        Float32::new(-self.value)
    }
}
impl Deref for Float32 {
    type Target = f32;
    fn deref(&self) -> &f32 {
        &self.value
    }
}
impl fmt::Display for Float32 {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(&self.value, f)
    }
}
impl fmt::Debug for Float32 {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Debug::fmt(&self.value, f)
    }
}
