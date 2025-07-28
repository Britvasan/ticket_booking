// // Copyright (c) 2025, Brit and contributors
// // For license information, please see license.txt

frappe.ui.form.on('Theatre', {
  refresh(frm) {
    //  Generate Layout button
    if (!frm.is_new()) {
      frm.add_custom_button('Generate Layout for Selected Screen', () => {
        const selected = frm.fields_dict['screen'].grid.get_selected_children();
        if (!selected.length) {
          frappe.msgprint(__('Select a screen row first'));
          return;
        }
        const row = selected[0];

        frappe.prompt([
          { fieldname: 'rows', label: 'Rows', fieldtype: 'Int', default: 10, reqd: 1 },
          { fieldname: 'per_row', label: 'Seats / Row', fieldtype: 'Int', default: 12, reqd: 1 },
          { fieldname: 'aisle_after', label: 'Aisle After Seat ', fieldtype: 'Int', default: 6, reqd: 1 }
        ], (value) => {
          frappe.call({
            method: 'cinema.cinema.api.generate_seat_layout',
            args: value,
            callback: r => {
              frappe.model.set_value(row.doctype, row.name,
                'seat_layout_json', r.message);
              frm.refresh_field('screen');
            }
          });
        }, 'Seat Layout Generator');
      });

      //  Preview Seats button  
      frm.add_custom_button('Preview Seat Map', () => {
        const selected = frm.fields_dict['screen'].grid.get_selected_children();
        if (!selected.length) {
          frappe.msgprint(__('Select a screen row first'));
          return;
        }
        const row = selected[0];
        const layout = JSON.parse(row.seat_layout_json || '{}');

        let html = '';
        (layout.rows || []).forEach(r => {
          html += `<div><strong>${r.row_label}</strong>: `
            + r.seats.map(s => `<span style="margin:2px;">🎟️ ${s.id}</span>`).join(' ')
            + `</div>`;
        });

        frappe.msgprint({ title: __('Seat Layout'), message: html, indicator: 'blue' });
      });
    }
  }
});
