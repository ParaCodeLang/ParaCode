extern crate proc_macro;
use proc_macro::TokenStream;

extern crate syn;
use syn::{parse_macro_input, DeriveInput};

extern crate quote;
use quote::quote;

#[proc_macro_derive(BasicValue)]
pub fn derive_basicvalue(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let st_name = input.ident;
    quote! {
        paracode::impl_basicvalue!(#st_name);
    }
    .into()
}

// #[proc_macro]
// pub fn generate_native_method(input: TokenStream) -> TokenStream {
//     // let input = parse_macro_input!(input as DeriveInput);
//     "fn answer() -> u32 { 42 }".parse().unwrap()
// }
