extern crate proc_macro;
use proc_macro::TokenStream;

extern crate syn;
use syn::{parse_macro_input, DeriveInput};

extern crate quote;
use quote::quote;

#[proc_macro_derive(BasicValue)]
pub fn derive_basicvalue(input: TokenStream) -> TokenStream {
    // "fn answer() -> u32 { 42 }".parse().unwrap()
    
    let input = parse_macro_input!(input as DeriveInput);
    let st_name = input.ident;
    // println!("{:?}", item);
    // "paracode::impl_basicvalue!(ASA)".parse().unwrap()
    quote! {
        paracode::impl_basicvalue!(#st_name);
    }.into()
}
