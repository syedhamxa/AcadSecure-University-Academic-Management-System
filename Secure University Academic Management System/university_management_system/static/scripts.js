document.addEventListener('DOMContentLoaded', ()=>{
  const reg = document.getElementById('regForm')
  if(reg){
    reg.addEventListener('submit', async e=>{
      e.preventDefault()
      const fd = new FormData(reg)
      const res = await fetch('/student/register',{method:'POST',body:fd})
      const j=await res.json(); alert(j.message)
    })
  }
  const publicReg = document.getElementById('publicRegisterForm')
  if(publicReg){
    publicReg.addEventListener('submit', async e=>{
      e.preventDefault()
      const role = publicReg.dataset.role || 'student'
      const fd = new FormData(publicReg)
      const res = await fetch('/register/' + role, {method:'POST', body: fd})
      const j = await res.json()
      alert(j.message)
      if(j.ok) window.location = '/login'
    })
  }
  const tbtn = document.getElementById('transcriptBtn')
  if(tbtn){
    tbtn.addEventListener('click', async ()=>{
      const r = await fetch('/student/transcript'); const j=await r.json();
      const win = window.open('','_blank')
      win.document.write('<pre>'+JSON.stringify(j,null,2)+'</pre>')
    })
  }
  const gform = document.getElementById('gradeForm')
  if(gform){
    gform.addEventListener('submit', async e=>{
      e.preventDefault(); const fd=new FormData(gform)
      const res = await fetch('/faculty/upload_grade',{method:'POST',body:fd}); const j=await res.json(); alert(j.message)
    })
  }
  const createUserForm = document.getElementById('createUserForm')
  if(createUserForm){
    createUserForm.addEventListener('submit', async e=>{
      e.preventDefault(); const fd=new FormData(createUserForm)
      const res = await fetch('/admin/create_user',{method:'POST',body:fd}); const j=await res.json(); alert(j.message)
    })
  }
  const createCourseForm = document.getElementById('createCourseForm')
  if(createCourseForm){
    createCourseForm.addEventListener('submit', async e=>{
      e.preventDefault(); const fd=new FormData(createCourseForm)
      const res = await fetch('/admin/create_course',{method:'POST',body:fd}); const j=await res.json(); alert(j.message)
    })
  }
  const assignForm = document.getElementById('assignForm')
  if(assignForm){
    assignForm.addEventListener('submit', async e=>{
      e.preventDefault(); const fd=new FormData(assignForm)
      const res = await fetch('/admin/assign_faculty',{method:'POST',body:fd}); const j=await res.json(); alert(j.message)
    })
  }
})
